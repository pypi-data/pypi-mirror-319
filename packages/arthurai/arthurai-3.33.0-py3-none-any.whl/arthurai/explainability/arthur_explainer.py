import logging
import re
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import skimage.segmentation as seg
from lime.explanation import Explanation
from lime.lime_image import LimeImageExplainer
from lime.lime_tabular import LimeTabularExplainer
from lime.lime_text import LimeTextExplainer
from shap import KernelExplainer

from arthurai import ArthurAttribute
from arthurai.common.constants import InputType, OutputType, Stage, TextDelimiter
from arthurai.common.exceptions import (
    ArthurUserError,
    MethodNotApplicableError,
    UnexpectedValueError,
    UserTypeError,
    UserValueError,
)
from arthurai.explainability.validation import (
    validate_predicted_attribute_order_matches_dataframe,
)

logger = logging.getLogger(__name__)


class EmptyLimeExplanation:
    """
    Class for representing an all-NaN LIME Explanation. The LIME Explainers return full-featured
    lime.explanation.Explanation objects. We only use these to fetch the feature importance scores for each predicted
    class by calling `as_map()`. This class implements that `as_map()` method, and returns all-NaN feature importance
    scores.
    """

    def __init__(self, class_int_labels: List[int], num_features: int):
        nans: List[Tuple[int, float]] = [
            (feat_idx, float("nan")) for feat_idx in range(num_features)
        ]
        self.nan_dict: Dict[int, List[Tuple[int, float]]] = {
            label: nans for label in class_int_labels
        }

    def as_map(self) -> Dict[int, List[Tuple[int, float]]]:
        """
        :return: A map from each predicted class integer label to a list of NaNs
        """
        return self.nan_dict


class ArthurExplainer:
    """Class for explaining inferences with a variety of libs"""

    SHAP = "shap"
    LIME = "lime"

    def __init__(
        self,
        model_type: OutputType,
        model_input_type: InputType,
        predicted_attributes: List[ArthurAttribute],
        predict_func: Callable,
        data: Optional[pd.DataFrame],
        label_mapping: List[Optional[Dict[str, int]]],
        categorical_features: Optional[List[int]] = None,
        enable_shap: bool = True,
        shap_training_samples: int = 20,
        enable_lime: bool = True,
        text_delimiter: TextDelimiter = TextDelimiter.NOT_WORD,
        load_image_func: Optional[Callable] = None,
        predictions_df: Optional[pd.DataFrame] = None,
        seed: Optional[int] = None,
    ):
        """
        :param model_type: Type of model being explained
        :param model_input_type: Type of input data, tabular, nlp, image
        :param predicted_attributes: the model's predicted attributes
        :param predict_func: callable, predict function for model
        :param data: Pandas DataFrame, required for tabular models
        :param label_mapping: A list of optional dictionaries. Each index corresponds to the feature index that will
            use the mapping
        :param categorical_features: A list of indices of the categorical features in the input data
        :param enable_shap: bool, should shap explanations be enabled, default true
        :param shap_training_samples: number of training samples to initialize shap
        :param enable_lime: bool, should Lime explanations be enabled, default true
        :param text_delimiter: TextDelimiter, the pattern used to split raw document into tokens, passed to `re.split`, default NOT_WORD
        :param load_image_func: image to load an image file and return an array of values
        :param predictions_df: DataFrame containing the model predictions for validation purposes
        :param seed: int, pre-defined seed to get consistent results from explainer, defaults to None which uses a random seed for each explanation
        """
        for attr in predicted_attributes:
            if attr.stage != Stage.PredictedValue:
                raise UnexpectedValueError(
                    f"Attribute {attr.name} in predicted_attributes parameter is of stage "
                    f"{attr.stage} not PredictedValue"
                )

        self.model_type = model_type
        self.model_input_type = model_input_type
        self.predicted_attributes = predicted_attributes
        self.input_predict_func = predict_func
        self.label_mapping = label_mapping
        self.categorical_features = categorical_features
        self.shap_training_samples = shap_training_samples
        self.reverse_label_mapping = [
            None if mapping is None else {val: key for key, val in mapping.items()}
            for mapping in self.label_mapping
        ]
        self.text_delimiter = text_delimiter
        self.load_image_func = load_image_func
        self.enable_shap = enable_shap
        self.enable_lime = enable_lime
        self.seed = seed

        self.positive_predicted_attr_position = None
        if len(self.predicted_attributes) == 2:
            positive_positions = [
                attr.position
                for attr in self.predicted_attributes
                if attr.is_positive_predicted_attribute
            ]
            if len(positive_positions) != 1:
                raise ArthurUserError(
                    "Must have exactly one positive predicted attribute"
                )
            self.positive_predicted_attr_position = positive_positions[0]

        # validate samples provided, image models don't require dataframe
        if model_input_type != InputType.Image:
            if data is None:
                raise UserTypeError(
                    f"Sample data must be provided for non-image models"
                )
            if predictions_df is None:
                raise UserTypeError(
                    f"Sample prediction data must be provided for non-image models"
                )

        # filter nans from data
        if data is not None:
            if predictions_df is None:
                raise UserTypeError(
                    f"Must provide prediction data if providing sample input data"
                )
            if len(data) != len(predictions_df):
                raise UnexpectedValueError(
                    f"Length of input data and predictions do not match"
                )
            data = data.reset_index(drop=True)
            predictions_df = predictions_df.reset_index(drop=True)

            length_with_nans = len(data)
            rows_without_nans = data.notna().all(axis=1)
            data = data[rows_without_nans]
            predictions_df = predictions_df[rows_without_nans]

            if len(data) != length_with_nans:
                logger.warning(
                    f"Dropped {length_with_nans - len(data)} rows with NaN values from explainer dataset"
                )

        # image models don't require dataframe
        if model_input_type != InputType.Image:
            # encode dataframe, don't save this as a instance variable for size
            encoded_data = pd.DataFrame(
                [self.encode_labels(fv) for fv in data.to_numpy()]
            )

            # run model predict wrapper on provided data
            logger.info(f"Testing model predict() function on provided data")
            try:
                actual_preds = self.predict_wrapper(encoded_data.to_numpy())
            except Exception as e:
                raise UserValueError(
                    f"Supplied predict() function failed for provided input, see exception "
                    f"above"
                ) from e
            # ensure that the prediction columns are in the correct order
            validate_predicted_attribute_order_matches_dataframe(
                actual_preds, predictions_df, self.predicted_attributes
            )
            logger.info(f"Model predict() function test successful")
        else:
            encoded_data = None

        self.tabular_explainer_shap = None
        self.tabular_explainer_lime = None

        # build tabular explainers
        if self.model_input_type == InputType.Tabular:
            self.build_tabular_explainers(
                enable_lime=self.enable_lime,
                enable_shap=self.enable_shap,
                data=encoded_data,
            )
        if self.model_input_type == InputType.NLP:
            if self.enable_shap:
                self.enable_shap = False
            # currently only Lime is supported for NLP, hardcode in args for now
            self.enable_lime = True
            self.build_nlp_explainers(
                enable_lime=self.enable_lime,
                enable_shap=self.enable_shap,
                data=encoded_data,
            )
        if self.model_input_type == InputType.Image:
            if self.load_image_func is None:
                raise UserValueError(
                    "load_image_func must be provided for image explanations"
                )
            if self.enable_shap:
                self.enable_shap = False
            # currently only Lime is supported for CV/ImageInput, hardcode in args for now
            self.enable_lime = True
            self.build_image_explainers(
                enable_lime=self.enable_lime,
                enable_shap=self.enable_shap,
                data=encoded_data,
            )
        # not supported input type
        else:
            pass

    @property
    def num_predicted_attributes(self) -> int:
        return len(self.predicted_attributes)

    def build_tabular_explainers(self, data: pd.DataFrame, **kwargs) -> None:
        try:
            if kwargs.get("enable_shap"):
                samples = (
                    data.sample(n=self.shap_training_samples, random_state=self.seed)
                    if len(data) > self.shap_training_samples
                    else data
                )
                shap_explainer = KernelExplainer(
                    model=self.predict_wrapper, data=samples, seed=self.seed
                )
                self.tabular_explainer_shap = shap_explainer

            if kwargs.get("enable_lime"):
                mode = (
                    "regression"
                    if self.model_type == OutputType.Regression
                    else "classification"
                )
                lime_explainer = LimeTabularExplainer(
                    training_data=data.to_numpy(),
                    mode=mode,
                    categorical_features=self.categorical_features,
                    discretize_continuous=False,
                    random_state=self.seed,
                )
                self.tabular_explainer_lime = lime_explainer
        except Exception:
            raise ArthurUserError(
                f"Failed to build explainer. "
                f"Please ensure your predict() function operates on batches, "
                f"taking in a sequence of inputs and returning an output in the format "
                f"appropriate for your model output predictions. For more info, consult "
                f"https://docs.arthur.ai/user-guide/walkthroughs/explainability.html#prediction-function"
            )

    def build_nlp_explainers(self, data: pd.DataFrame, **kwargs) -> None:
        # shap not supported at this time
        if kwargs.get("enable_shap"):
            pass

        if kwargs.get("enable_lime"):
            # we always default to no bow so we get one explanation per word
            lime_explainer = LimeTextExplainer(
                bow=False,
                split_expression=self.text_delimiter,
                random_state=self.seed,
            )
            self.nlp_explainer_lime = lime_explainer

    def build_image_explainers(self, data: pd.DataFrame, **kwargs) -> None:
        if kwargs.get("enable_shap"):
            pass

        if kwargs.get("enable_lime"):
            lime_explainer = LimeImageExplainer(random_state=self.seed)
            self.image_explainer_lime = lime_explainer

    def encode_labels(self, feature_vector: Iterable) -> Iterable:
        """Encodes labels into integers"""
        encoded_fv = []
        for i, val in enumerate(feature_vector):
            cur_label_mapping = self.label_mapping[i]
            if cur_label_mapping is not None:
                # if this is a categorical value that isn't captured by attribute categories
                # update mapping to handle gracefully
                if val not in cur_label_mapping:
                    new_mapped_val = max(cur_label_mapping.values()) + 1
                    cur_label_mapping[val] = new_mapped_val
                    # add value to reverse label mapping as well, so we can decode
                    self.reverse_label_mapping[i][new_mapped_val] = val  # type: ignore
                encoded_fv.append(cur_label_mapping[val])
            else:
                encoded_fv.append(val)
        return encoded_fv

    def decode_labels(self, feature_vector: Iterable) -> Iterable:
        """Decodes into strings"""
        decoded_fv = []
        for i, val in enumerate(feature_vector):
            cur_reverse_label_mapping = self.reverse_label_mapping[i]
            if cur_reverse_label_mapping is not None:
                decoded_fv.append(cur_reverse_label_mapping[val])
            else:
                decoded_fv.append(val)
        return decoded_fv

    def predict_wrapper(self, encoded_feature_vectors: Iterable) -> np.ndarray:
        """Wraps user supplied predict function. Handles decoding back into original format.
        For binary classifiers, checks the output size and reshapes to two dimensions if necessary
        """
        decoded_feature_vectors = encoded_feature_vectors
        if self.model_input_type == InputType.Tabular:
            decoded_feature_vectors = [
                self.decode_labels(fv) for fv in encoded_feature_vectors
            ]

        output = np.array(self.input_predict_func(decoded_feature_vectors))
        if (
            self.model_type == OutputType.Multiclass
            and self.num_predicted_attributes == 2
        ):  # binary classifier
            if len(output.shape) == 1:  # reshape to 2D array
                output = output.reshape((output.shape[0], 1))
            if output.shape[1] == 1:  # check if single predict output
                if self.positive_predicted_attr_position == 0:
                    return np.hstack([output, 1 - output])
                elif self.positive_predicted_attr_position == 1:
                    return np.hstack([1 - output, output])
                else:
                    raise ArthurUserError(
                        "Positive predicted attr position must be 0 or 1"
                    )
        return output

    def predict_tabular(self, input_feature_vectors: List[List[Any]]) -> np.ndarray:
        """Takes in customer provided data and returns the prediction values as numpy array (both regression and classification)"""
        # check if model type is tabular
        if self.model_input_type != InputType.Tabular:
            raise MethodNotApplicableError(
                f"Cannot run a {InputType.Tabular} prediction on a {self.model_input_type} model"
            )

        try:
            # encode input features to pass into predict_wrapper()
            encoded_features = np.array(
                [self.encode_labels(fv) for fv in input_feature_vectors],
                dtype=np.float64,
            )

            # use predict wrapper to handle decoding and additional processing
            predictions = self.predict_wrapper(encoded_features)
        except Exception:
            raise UserValueError(
                "Could not make prediction(s) based on input - please ensure data is properly "
                "formatted and has the necessary features"
            )
        return predictions

    def shap_expected_values(self) -> List[float]:
        """Returns expected values from the shap explainer for this model input type"""
        if self.model_input_type == InputType.Tabular:
            shap_explainer = self.tabular_explainer_shap
        # other model types not supported ATM
        else:
            raise UserValueError(
                f"This explainer does not have {self.SHAP} configured "
                f"for the model type: {self.model_input_type}"
            )

        if shap_explainer is None:
            raise UserValueError(
                f"{self.SHAP} explanations are not enabled for this explainer"
            )

        exp_values = shap_explainer.expected_value

        # always return a list even if one predicted value
        if type(exp_values) == np.ndarray:
            exp_values = exp_values.tolist()
        else:
            exp_values = [exp_values]

        return exp_values

    def explain_tabular_shap(
        self, raw_feature_vectors: List, **kwargs
    ) -> List[List[List[float]]]:
        """Calculate SHAP values. For one or more inferences.

        :param raw_feature_vectors: An iterable of one or more feature vectors to explain.
        :param kwargs: Additional args to pass to SHAP.

        :return: A List of explanations for each feature vector. A single explanation is a list of lists that contain
            the explanation for each model output by input feature. In this example, the model has 4 features and
            3 output classes.

            .. code-block:: python

                [
                    [-0.011, 0.009, -0.128, -0.161],
                    [-0.009, 0.003, -0.091, -0.065],
                    [0.02, -0.013, 0.220, 0.226]
                ]

        """

        if self.model_input_type != InputType.Tabular:
            raise MethodNotApplicableError(
                f"Cannot run a {InputType.Tabular} explanation on a {self.model_input_type} model"
            )

        if self.tabular_explainer_shap is None:
            raise MethodNotApplicableError(
                f"Tabular {self.SHAP} explanations are not enabled for this explainer"
            )

        # swap strings for integers using lookup table
        feature_vectors = np.array(
            [self.encode_labels(fv) for fv in raw_feature_vectors], dtype=np.float64
        )
        explanations = self.tabular_explainer_shap.shap_values(
            feature_vectors, **kwargs
        )

        # format by inference not by class
        if type(explanations) == np.ndarray:
            explanations = [explanations]

        # create 2D array result lists for each inference to organize by inference
        # instead of by class
        results_by_inference = []
        for _ in range(len(raw_feature_vectors)):
            results_by_inference.append([])

        for explanation in explanations:
            explanation_list = explanation.tolist()
            for i, row in enumerate(explanation_list):
                results_by_inference[i].append(row)

        return results_by_inference

    def explain_tabular_lime(
        self, raw_feature_vectors: List, **kwargs
    ) -> List[List[List[float]]]:
        """
        Calculate lime values. For one or more inferences.

        :param raw_feature_vectors: An iterable of one or more feature vectors to explain.
        :param kwargs: Additional args to pass to LIME.
        :return: A List of explanations for each feature vector. A single explanation is
            a list of lists that contain the explanation for each model output by input feature.
            In this example, the model has 4 features and 3 output classes:

            .. code-block:: python

                [
                    [
                        [-0.011, 0.009, -0.128, -0.161],
                        [-0.009, 0.003, -0.091, -0.065],
                        [0.02, -0.013, 0.220, 0.226]
                    ]
                ]
        """

        if self.model_input_type != InputType.Tabular:
            raise MethodNotApplicableError(
                f"Cannot run a {InputType.Tabular} explanation on a {self.model_input_type} model"
            )

        if self.tabular_explainer_lime is None:
            raise MethodNotApplicableError(
                f"Tabular {self.LIME} explanations are not enabled for this explainer"
            )

        # explain all features and classes
        num_features = len(raw_feature_vectors[0])
        if self.model_type == OutputType.Regression:
            # ignored by lime for regression
            labels = [1]
        else:
            # for classification, lime returns
            # results by label in the range 0 to (n-1)
            labels = list(range(self.num_predicted_attributes))

        # swap strings for integers using lookup table
        feature_vectors = np.array(
            [self.encode_labels(fv) for fv in raw_feature_vectors], dtype=np.float64
        )

        explanations: List[Union[Explanation, EmptyLimeExplanation]] = []
        for feature_vector in feature_vectors:
            # if there are any NaNs in this feature, return all NaNs as the explanation
            if np.any(np.isnan(feature_vector)):
                exp = EmptyLimeExplanation(
                    class_int_labels=labels, num_features=num_features
                )
            else:
                exp = self.tabular_explainer_lime.explain_instance(
                    feature_vector,
                    self.predict_wrapper,
                    num_features=num_features,
                    labels=labels,
                    **kwargs,
                )
            explanations.append(exp)

        return self.format_lime_results(explanations)

    def explain_tabular(
        self,
        algo: str,
        raw_feature_vectors: List,
        nsamples: Optional[int] = None,
        **kwargs,
    ) -> List[List[List[float]]]:
        if self.model_input_type != InputType.Tabular:
            raise MethodNotApplicableError(
                f"Cannot run a {InputType.Tabular} explanation on a {self.model_input_type} model"
            )

        if algo == self.SHAP:
            # shap takes nsamples
            if nsamples is not None:
                kwargs["nsamples"] = nsamples
            return self.explain_tabular_shap(
                raw_feature_vectors=raw_feature_vectors, **kwargs
            )

        elif algo == self.LIME:
            # lime takes num_samples
            if nsamples is not None:
                kwargs["num_samples"] = nsamples
            return self.explain_tabular_lime(
                raw_feature_vectors=raw_feature_vectors, **kwargs
            )

        # other algos not supported ATM
        else:
            raise UserValueError(
                f"This explainer does not know how to explain {algo} "
                f"for the model type: {self.model_input_type}"
            )

    def explain_nlp_lime(
        self, raw_feature_vectors: List, **kwargs
    ) -> List[List[List[List[float]]]]:
        if self.model_input_type != InputType.NLP:
            raise MethodNotApplicableError(
                f"Cannot run a {InputType.NLP} explanation on a {self.model_input_type} model"
            )

        if self.nlp_explainer_lime is None:
            raise MethodNotApplicableError(
                f"Tabular {self.LIME} explanations are not enabled for this explainer"
            )

        # explain all features and classes
        if self.model_type == OutputType.Regression:
            # ignored by lime for regression
            labels: Iterable = (1,)
        else:
            # for classification, lime returns
            # results by label in the range 0 to (n-1)
            labels = list(range(self.num_predicted_attributes))

        explanations = []
        for feature_vector in raw_feature_vectors:
            if len(feature_vector) != 1:
                raise UserValueError(
                    "Cannot use NLP explainer with more than 1 feature"
                )

            # get number of unique words to ensure we get explanation for each word
            num_features = len(re.split(self.text_delimiter, feature_vector[0]))

            # 5000 is default value from Lime
            num_samples = kwargs.get("num_samples") if "num_samples" in kwargs else 5000
            exp = self.nlp_explainer_lime.explain_instance(
                feature_vector[0],
                self.predict_wrapper,
                labels=labels,
                num_features=num_features,
                num_samples=num_samples,
            )
            explanations.append(exp)

        return self.format_lime_text_results(explanations)

    def explain_nlp(
        self,
        algo: str,
        raw_feature_vectors: List,
        nsamples: Optional[int] = None,
        **kwargs,
    ) -> List[List[List[List[float]]]]:
        if self.model_input_type != InputType.NLP:
            raise MethodNotApplicableError(
                f"Cannot run a {InputType.NLP} explanation on a {self.model_input_type} model"
            )

        if algo == self.SHAP:
            raise UserValueError(
                f"SHAP explainers are not supported at this time for NLP models"
            )
        elif algo == self.LIME:
            # lime takes num_samples
            if nsamples is not None:
                kwargs["num_samples"] = nsamples
            return self.explain_nlp_lime(
                raw_feature_vectors=raw_feature_vectors, **kwargs
            )
        else:
            raise UserValueError(
                f"This explainer does not know how to explain {algo} "
                f"for the model type: {self.model_input_type}"
            )

    def explain_image_lime(self, image_paths: List, **kwargs) -> List[Dict[str, Any]]:
        if self.model_input_type != InputType.Image:
            raise MethodNotApplicableError(
                f"Cannot run a {InputType.Image} explanation on a {self.model_input_type} model"
            )

        if self.image_explainer_lime is None:
            raise MethodNotApplicableError(
                f"Image {self.LIME} explanations are not enabled for this explainer"
            )

        if self.load_image_func is None:
            raise MethodNotApplicableError("load_image function has not been provided")

        # explain all features and classes
        if self.model_type == OutputType.Regression:
            # ignored by lime for regression
            labels: Iterable = (1,)
        else:
            # for classification, lime returns
            # results by label in the range 0 to (n-1)
            labels = list(range(self.num_predicted_attributes))

        explanations = []

        # Add code to default the number of segments for any give image to be 40
        def segmentation_slic_func(original_image):
            DEFAULT_NUM_SEGMENTS = 40
            return seg.slic(original_image, DEFAULT_NUM_SEGMENTS)

        for image_path in image_paths:
            image = self.load_image_func(image_path)
            # 5000 is default value from Lime
            num_samples = kwargs.get("num_samples") if "num_samples" in kwargs else 5000
            exp = self.image_explainer_lime.explain_instance(
                image,
                self.predict_wrapper,
                labels=labels,
                num_samples=num_samples,
                segmentation_fn=segmentation_slic_func,
            )
            explanations.append(exp)

        return self.format_lime_image_results(explanations)

    def explain_image(
        self, algo: str, image_paths: List, nsamples: Optional[int] = None, **kwargs
    ) -> List[Dict[str, Any]]:
        if self.model_input_type != InputType.Image:
            raise MethodNotApplicableError(
                f"Cannot run a {InputType.Image} explanation on a {self.model_input_type} model"
            )

        if algo == self.SHAP:
            raise UserValueError(
                f"SHAP explainers are not supported at this time for CV/ImageInput models"
            )
        elif algo == self.LIME:
            # lime takes num_samples
            if nsamples is not None:
                kwargs["num_samples"] = nsamples
            return self.explain_image_lime(image_paths=image_paths, **kwargs)
        else:
            raise UserValueError(
                f"This explainer does not know how to explain {algo} "
                f"for the model type: {self.model_input_type}"
            )

    @staticmethod
    def format_lime_results_for_one_class(
        feature_index_score_pairs: List[Tuple[int, float]]
    ) -> List[float]:
        """
        This method unpacks the results for a single classes's explanation:

            .. code-block:: python

                [
                    (3, -0.1614709564346036),
                    (2, -0.12871035938256958),
                    (0, -0.011225126011010974),
                    (1, 0.009948039509525414)
                ]

        :return: unpacked lime results for a single class

            .. code-block:: python

                [-0.011, 0.009, -0.128, -0.161]

        """
        feature_index_score_pairs_sorted = sorted(
            feature_index_score_pairs, key=lambda x: x[0]
        )
        return [score[1] for score in feature_index_score_pairs_sorted]

    def format_lime_results(
        self, results: List[Union[Explanation, EmptyLimeExplanation]]
    ) -> List[List[List[float]]]:
        """
        LIME's .as_map() method returns scores looking like the following:

            .. code-block:: python

                {
                   0:[
                      (3, -0.1614709564346036),
                      (2, -0.12871035938256958),
                      (0, -0.011225126011010974),
                      (1, 0.009948039509525414)
                   ],
                   1:[
                      (2, -0.0914379318506283),
                      (3, -0.06513690080871648),
                      (0, -0.009164069675758498),
                      (1, 0.003622751782692439)
                   ],
                   2:[
                      (3, 0.2266078572433201),
                      (2, 0.22014829123319787),
                      (0, 0.02038919568676947),
                      (1, -0.013570791292217853)
                   ]
                }

        Where the keys are the class labels, and the values are lists of feature index, score tuples for that class.

        This method unpacks the result to a list of lists for EACH explanation:

            .. code-block:: python

                [
                    [-0.011, 0.009, -0.128, -0.161],
                    [-0.009, 0.003, -0.091, -0.065],
                    [0.02, -0.013, 0.220, 0.226]
                ]

        For regression, this will return a list of lists for one class per inference:

            .. code-block:: python

                [
                    [-0.011, 0.009, -0.128, -0.161]
                ]

        """
        formatted_explanations = []
        for expl in results:
            if self.model_type == OutputType.Regression:
                # lime returns regression scores under the class label key 1
                scores: List[Any] = self.format_lime_results_for_one_class(
                    feature_index_score_pairs=expl.as_map()[1]
                )
                # wrap regression scores in a list because there's only 1 model output
                formatted_explanations.append([scores])

            else:
                sorted_class_score_pairs = sorted(
                    list(expl.as_map().items()), key=lambda x: x[0]
                )
                scores = []
                for class_index, feature_index_score_pairs in sorted_class_score_pairs:
                    scores_for_class = self.format_lime_results_for_one_class(
                        feature_index_score_pairs=feature_index_score_pairs
                    )
                    scores.append(scores_for_class)
                formatted_explanations.append(scores)

        return formatted_explanations

    def format_lime_text_results(
        self, results: List[Explanation]
    ) -> List[List[List[List[float]]]]:
        """Format LIME results for Text models

        LIME's .as_map() method returns scores looking like the following:

        .. code-block:: python

            {0: [('I', -0.1614709564346036), ('a', -0.12871035938256958), ('am', -0.011225126011010974), ('developer', 0.009948039509525414)],
             1: [('am', -0.0914379318506283), ('a', -0.06513690080871648), ('I', -0.009164069675758498), ('developer', 0.003622751782692439)],
             2: [('developer', 0.2266078572433201), ('am', 0.22014829123319787), ('a', 0.02038919568676947), ('I', -0.013570791292217853)]}

        Where the keys are the class labels, and the values are lists of word, score tuples for that class.

        This method unpacks the result to a list of lists for EACH explanation:

        .. code-block:: python

            [
                [['I', -0.011], ['am', 0.009], ['a', -0.128], ['developer', -0.161]],
                [['I', -0.02], ['am', 0.007], ['a', -0.8], ['developer', 0.11]],
                [['I', -0.03], ['am', 0.89], ['a', -0.28], ['developer', -0.16]]
            ]

        For regression, this will return a list of lists for one class per inference:

        .. code-block:: python

            [
                [['I', -0.011], ['am', 0.009], ['a', -0.128], ['developer', -0.161]]
            ]

        :return: formatted results in the following format

            .. code-block:: python

                [
                    [['I', -0.011], ['am', 0.009], ['a', -0.128], ['developer', -0.161]],
                    [['I', -0.02], ['am', 0.007], ['a', -0.8], ['developer', 0.11]],
                    [['I', -0.03], ['am', 0.89], ['a', -0.28], ['developer', -0.16]]
                ]
        """
        formatted_explanations = []
        for exp in results:
            # lime returns explanations with indices, need to map back to token
            raw_map = exp.as_map()
            final_map = {}
            for key in raw_map.keys():
                id_scores = raw_map[key]
                word_scores = exp.domain_mapper.map_exp_ids(id_scores)

                # lime loses ordering, so we have to re-order by position
                word_score_pos = []
                for id_score, word_score in zip(id_scores, word_scores):
                    _id = id_score[0]
                    pos = exp.domain_mapper.indexed_string.string_position(_id)
                    # convert tuples to lists
                    word_score_pos.append((pos, list(word_score)))

                sorted_by_pos = sorted(word_score_pos, key=lambda x: x[0])
                final_map[key] = [x[1] for x in sorted_by_pos]

            if self.model_type == OutputType.Regression:
                # lime stores regression results under class label 1
                formatted_explanations.append([final_map[1]])
            else:
                # if multiple classes, get as a list and sort by class
                # results in [ (class, [scores]), (class, [scores]) ]
                sorted_class_score_pairs = sorted(
                    list(final_map.items()), key=lambda x: x[0]
                )
                # pull out just scores from each tuple
                fmt_exp = [x[1] for x in sorted_class_score_pairs]
                formatted_explanations.append(fmt_exp)

        return formatted_explanations

    @staticmethod
    def format_lime_image_results(results: List[Explanation]) -> List[Dict[str, Any]]:
        """Format LIME results for images

        :returns: formatted output in the following format:

            .. code-block:: python

                {
                    "lime_segment_mask": [
                        [1, 1, 1, 3, 3, 1, 0],
                        [1, 1, 1, 3, 3, 1, 0],
                        [1, 1, 1, 3, 3, 1, 0],
                        [2, 2, 2, 3, 3, 1, 0]
                    ],
                    "lime_region_mapping": {
                        "0": [[0, 0.23], [1, 0.3], [2, 0.001], [3, -0.5]]
                    }
                }
        """
        formatted_explanations = []
        for explanation in results:
            region_scores = explanation.local_exp
            new_region_scores = {}
            for k, v in region_scores.items():
                new_key = str(k.item()) if isinstance(k, np.generic) else str(k)
                new_vals = []
                for val in v:
                    new_val = np.array(val).tolist()
                    new_vals.append(new_val)
                new_region_scores[new_key] = new_vals

            formatted_explanations.append(
                {
                    "lime_segment_mask": explanation.segments.tolist(),
                    "lime_region_mapping": new_region_scores,
                }
            )

        return formatted_explanations
