import json
import logging
import os
import re
import shutil
import sys
import tempfile
import time
from dataclasses import InitVar, dataclass, field
from datetime import datetime, timedelta
from http import HTTPStatus
from io import BufferedRandom, BufferedReader
from math import ceil
from os import PathLike
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import numpy as np
import pytz
import shortuuid
from dateutil.parser import ParserError
from pandas import CategoricalDtype, DataFrame, Series, isna

from arthurai import util as arthur_util
from arthurai.client import validation
from arthurai.client.http.requests import HTTPClient
from arthurai.common.constants import (
    API_PREFIX,
    API_PREFIX_V4,
    AccuracyMetric,
    Enrichment,
    IMAGE_FILE_EXTENSION_MAP,
    ImageResponseType,
    InferenceType,
    InputType,
    ModelStatus,
    ONBOARDING_SPINNER_MESSAGE,
    ONBOARDING_UPDATE_MESSAGE,
    OutputType,
    PARQUET_INGESTIBLE_INPUT_TYPES,
    PARQUET_INGESTIBLE_OUTPUT_TYPES,
    Stage,
    TextDelimiter,
    TimestampInferenceType,
    ValueType,
)
from arthurai.common.exceptions import (
    ArthurUnexpectedError,
    ArthurUserError,
    ExpectedParameterNotFoundError,
    MethodNotApplicableError,
    MissingParameterError,
    UnexpectedTypeError,
    UserTypeError,
    UserValueError,
    arthur_excepted,
)
from arthurai.core import inferences as inferences_util, util as core_util
from arthurai.core.alerts import (
    Alert,
    AlertRule,
    AlertRuleBound,
    AlertRuleSeverity,
    AlertStatus,
    Metric,
    MetricType,
    validate_parameters_for_alert,
)
from arthurai.core.attributes import (
    ArthurAttribute,
    AttributeBin,
    AttributeCategory,
    get_attribute_order_stage,
)
from arthurai.core.base import ArthurBaseJsonDataclass, NumberType
from arthurai.core.bias.bias_wrapper import ArthurBiasWrapper
from arthurai.core.data_service import DatasetService, ImageZipper
from arthurai.core.dataset_validation_utils import (
    valid_rec_obj,
    validate_attr_names,
    validate_series_data_type,
)
from arthurai.core.enrichment_status_waiter import await_enrichments_ready
from arthurai.core.inferences import FALSE_DEFAULT_IGNORE_JOIN_ERRORS
from arthurai.core.model_status_waiter import ModelStatusWaiter
from arthurai.core.model_utils import (
    _get_json_data,
    _get_parquet_file,
    _image_attr,
    _text_attr,
    _token_likelihoods_attr,
    _tokens_attr,
)
from arthurai.core.util import is_list_like, is_str_like, update_column_in_list_of_dicts
from arthurai.core.viz.visualizer import DataVisualizer
from arthurai.explainability.explanation_packager import ExplanationPackager
from arthurai.version import __version__

logger = logging.getLogger(__name__)

INFERENCE_DATA_RETRIES = 3
MAX_ATTRIBUTES_TO_SHOW = 10
AUTO_CATEGORICAL_MAX = 25


@dataclass
class ExplainabilityParameters(ArthurBaseJsonDataclass):
    enabled: bool
    explanation_algo: Optional[str] = None
    model_server_cpu: Optional[str] = None
    model_server_memory: Optional[str] = None
    explanation_nsamples: Optional[int] = None


@dataclass
class ArthurModel(ArthurBaseJsonDataclass):
    """
    Arthur Model class represents the metadata which represents a registered model in the application

    :param client: :class:`arthurai.client.Client` object which manages data storage
    :param partner_model_id: Client provided unique id to associate with the model. This field must be unique across
                             all active models cannot be changed once set.
    :param input_type: :class:`arthurai.common.constants.InputType` representing the model's input data type.
    :param output_type: :class:`arthurai.common.constants.OutputType` representing the model's output data format.
    :param explainability:  :class:`arthurai.core.models.ExplainabilityParameters` object representing parameters that
                            will be used to create inference explanations.
    :param id: The auto-generated unique UUID for the model. Will be overwritten if set by the user.
    :param display_name: An optional display name for the model.
    :param description: Optional description of the model.
    :param is_batch: Boolean value to determine whether the model sends inferences in batch or streaming format.
                     Defaults to False.
    :param archived: Indicates whether or not a model has been archived, defaults to false.
    :param created_at: UTC timestamp in ISO8601 format of when the model was created. Will be overwritten if set by the
                       user.
    :param updated_at: UTC timestamp in ISO8601 format of when the model was last updated. Will be overwritten if set by
                       the user.
    :param attributes: List of :class:`arthurai.core.attributes.ArthurAttribute` objects registered to the model
    :param tags: List of string keywords to associate with the model.
    :param classifier_threshold: Threshold value for classification models, default is 0.5.
    :param text_delimiter: Only valid for models with input_type equal to
                           :py:attr:`arthurai.common.constants.InputType.NLP`. Represents the text delimiter
                           to divide input strings.
    :param expected_throughput_gb_per_day: Expected amount of throughput.
    :param pixel_height: Only valid for models with input_type equal to
                           :py:attr:`arthurai.common.constants.InputType.Image`. Expected image height in pixels.
    :param pixel_width: Only valid for models with input_type equal to
                           :py:attr:`arthurai.common.constants.InputType.Image`. Expected image width in pixels.
    :param status: Indicates the current status of the model. See the Arthur documentation below for an `in-depth
                   explanation`_ of each status.

    .. _in-depth explanation: https://docs.arthur.ai/user-guide/basic_concepts.html#onboarding-status
    """

    partner_model_id: str
    input_type: InputType
    output_type: OutputType
    # This is just used during init and will not be associated with
    # an instance of this class, instead reference ArthurModel._client
    client: InitVar[Optional[HTTPClient]] = None
    explainability: Optional[ExplainabilityParameters] = None
    id: Optional[str] = None
    display_name: Optional[str] = None
    description: Optional[str] = None
    is_batch: bool = False
    archived: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    attributes: Optional[List[ArthurAttribute]] = None
    tags: Optional[List[str]] = None
    classifier_threshold: Optional[float] = None
    text_delimiter: Optional[TextDelimiter] = None
    expected_throughput_gb_per_day: Optional[int] = None
    pixel_height: Optional[int] = None
    pixel_width: Optional[int] = None
    image_class_labels: Optional[List[str]] = None
    status: Optional[ModelStatus] = None

    # Model Group properties
    model_group_id: Optional[str] = None
    version_sequence_num: Optional[int] = None
    version_label: Optional[str] = None

    # from model utils
    # (https://www.jetbrains.com/help/pycharm/disabling-and-enabling-inspections.html#suppress-inspections)
    # noinspection PyUnresolvedReferences
    from arthurai.core.model_utils import (
        check_attr_is_bias,
        check_has_bias_attrs,
        get_positive_predicted_class,
    )

    def __post_init__(self, client: HTTPClient):
        """
        Special initialization method for dataclasses that is called after the generated __init__() method.

        Input parameters to __post_init__ (may) be parsed out of the class variables and into this
        method. E.g. defining ArthurModel.client allows you to create an ArthurModel instance as
        `ArthurModel(client=...)` where client is only passed into __post_init__ and does not show
        up as an instance variable. To do so, the class variable type must be defined with an
        InitVar[] wrapper (refer to link to Python docs below).
        https://docs.python.org/3/library/dataclasses.html#init-only-variables

        Variables created here will only be accessible directly on the object itself, they will not
        be in the result of object.to_dict() even if marked as public (does not have preceding
        underscore).
        """
        self._client = client
        self._explainer: Optional[ExplanationPackager] = None
        self.viz = DataVisualizer([self])
        self.attributes_type_dict = {}
        if self.attributes is not None:
            for attr in self.attributes:
                self.attributes_type_dict[attr.name] = attr.value_type
            # sort by stage, followed by position
            self.attributes.sort(
                key=lambda x: (
                    get_attribute_order_stage(x.stage),
                    x.position if x.position is not None else 0,
                )
            )
        self.bias = ArthurBiasWrapper(self)
        self._store_model_id_in_env()
        self._ground_truth_type = None  # indicates whether model uses the GroundTruthClass or GroundTruth stage
        self.reference_dataframe: Optional[DataFrame] = None

    def __str__(self):
        name = (
            f"{str(self.input_type).capitalize()} {str(self.output_type).capitalize()} Model\n"
            f"\t{self.display_name}:{self.partner_model_id}"
        )
        if self.model_group_id:
            # TODO: can you have version without model group and vice versa
            name += f"@{self.model_group_id}:{self.version_label}"

        current_stage = "Local"
        if self.model_is_saved():
            current_stage = "Production"
        name += f"\n\tStage: {current_stage}"

        string_attributes = []
        for attr in self.attributes[:MAX_ATTRIBUTES_TO_SHOW]:
            string_attributes.append(attr.short_name())
        name += f"\n\tAttributes: {string_attributes}"

        if len(self.attributes) > MAX_ATTRIBUTES_TO_SHOW:
            name += f"... and {len(self.attributes) - MAX_ATTRIBUTES_TO_SHOW} more"

        return name

    @property
    def ground_truth_type(self) -> Optional[Stage]:
        """
        Returns `GroundTruthClass` if Arthur performed one-hot encoding
        in the creation of this model's current ground truth attribute.
        Otherwise, returns `GroundTruth`.

        The `GroundTruthClass` stage is an Arthur-generated stage of attributes,
        which are made after one-hot encoding attributes of the GroundTruth stage.
        """
        if self._ground_truth_type:
            return self._ground_truth_type
        else:
            if self.attributes is None:
                return None
            self._ground_truth_type = (
                Stage.GroundTruthClass
                if Stage.GroundTruthClass in [attr.stage for attr in self.attributes]
                else Stage.GroundTruth
            )
        return self._ground_truth_type

    @arthur_excepted("failed to save model")
    def save(self, skip_validation: bool = False) -> str:
        """Check and save this model

        After this method is called successfully, your model is sent to the Arthur Platform where all its data and
        metrics are saved. The method will start an async call to get the model ready to accept inferences and will
        run a spinner until model reaches :py:attr:`~arthurai.common.constants.ModelStatus.Ready` or
        :py:attr:`~arthurai.common.constants.ModelStatus.CreationFailed` state. If you cancel the call when the
        spinner is running, the model is still being provisioned and does not cancel model onboarding. You won't be
        able to send inferences until model reaches :py:attr:`~arthurai.common.constants.ModelStatus.Ready` state. You
        can use await_model_ready() method to wait for it.

        If the model onboarding fails, you can execute this method again to retry model onboarding.

        Returns the model's ID in the Arthur platform once the upload is successful.

        .. code-block:: python

            model_id = arthur_model.save()
            with open("fullguide_model_id.txt", "w") as f:
                f.write(model_id) # saving this model's id to a local file

        :return: The model id
        :param: skip_validation: opt out of reference dataset validation. Defaults to False. Set to True to force an attempt to save your model regardless of errors raised in :py:func:`validate_reference_data()`.

        :raises MethodNotApplicableError: the model has already been saved
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: model write AND (usually) reference_data write
        """
        # validate reference data set against model schema
        if self.reference_dataframe is not None and not skip_validation:
            self.validate_reference_data(self.reference_dataframe)

        # if the model has not been set yet
        if self.id is None:
            self._save_and_provision_model()
        elif self.status == ModelStatus.CreationFailed:
            self._retry_model_provisioning()
        elif self.status == ModelStatus.Creating or self.status == ModelStatus.Pending:
            raise MethodNotApplicableError(
                "This model is still provisioning, please use await_model_ready() call to "
                "wait for the provisioning to complete"
            )
        else:
            raise MethodNotApplicableError(
                "Cannot save a registered model; use update instead."
            )

        # set reference data if it's waiting to be sent
        if self.reference_dataframe is not None:
            self.set_reference_data(data=self.reference_dataframe)
            # don't need to keep it around anymore
            self.reference_dataframe = None

        return self.id  # type: ignore

    def validate_reference_data(self, reference_dataframe: DataFrame) -> None:
        """Validate the reference dataset against the model schema

        This method validates the reference dataset by raising errors when the reference dataset and the model schema
        don't match (either the column data type doesn't match the corresponding attribute's Arthur Value Type, or
        the columns and attributes do not have the same names) or the reference dataset can't be serialized to parquet
        files. It logs a warning when a column's data type can't be validated because of None or empty objects.

        :param: reference_dataframe: A DataFrame containing the reference data.
        :raises: UserTypeError: Error message contains the list of all found validation errors.
        """

        errors = []
        columns_unique, columns_duplicate, unexpected_cols, missing_cols = (
            set(),
            set(),
            set(),
            set(),
        )
        attribute_names = (
            set([attribute.name for attribute in self.attributes])
            if self.attributes is not None
            else set()
        )

        if not isinstance(reference_dataframe, DataFrame):
            raise UserTypeError(
                f"Parameter `reference_dataframe` is not a DataFrame. `validate_reference_data()` "
                f"only validates reference datasets passed as DataFrames against the model schema."
            )
        elif reference_dataframe is None or len(reference_dataframe) == 0:
            raise UserTypeError(
                f"Parameter `reference_dataframe` is None or an empty DataFrame. The model schema "
                f"cannot be validated against it."
            )

        # validate columns and attributes are the same
        for col in reference_dataframe.columns.values:
            if col not in columns_unique:
                columns_unique.add(col)
            else:
                columns_duplicate.add(col)
                columns_unique.remove(col)
            if col not in attribute_names:
                unexpected_cols.add(col)
        if len(columns_duplicate) > 0:  # dataset has duplicate column names
            errors.append(
                "Your reference dataset has duplicate column(s) with the same name. Please resolve "
                f"before saving for the following column(s): {str(columns_duplicate)[1:-1]}"
            )
        elif (
            attribute_names != columns_unique
        ):  # dataset columns are not the same as expected attributes
            missing_cols = attribute_names - columns_unique
            if len(missing_cols) > 0:
                errors.append(
                    f"Column(s) {str(missing_cols)[1:-1]} are expected by your model schema but not in your "
                    "reference dataset. If you want to onboard your model anyway, please add a column with "
                    "None objects to explicitly indicate the missing data."
                )
            if len(unexpected_cols) > 0:
                errors.append(
                    f"Column(s) {str(unexpected_cols)[1:-1]} are in your reference dataset but were not expected "
                    "by your model schema."
                )

        # validate column names:
        try:
            validate_attr_names(reference_dataframe.columns)
        except UserValueError as e:
            errors.append(str(e))

        # validate data types are as expected
        attributes = self.attributes if self.attributes is not None else set()
        for attr in attributes:
            if attr.name in columns_unique:  # ensures col is in dataframe
                try:
                    validate_series_data_type(
                        reference_dataframe[attr.name], attr
                    )  # validate data type mismatch
                except (UserValueError, UserTypeError) as e:
                    errors.append(str(e))

        # validate reference Dataframe can serialize to parquet for parquet ingestible model types
        if (
            self.input_type in PARQUET_INGESTIBLE_INPUT_TYPES
            and self.output_type in PARQUET_INGESTIBLE_OUTPUT_TYPES
        ):
            try:
                with tempfile.TemporaryDirectory() as source_directory:
                    path = os.path.join(
                        source_directory, f"test-valid-serialization.parquet"
                    )
                    reference_dataframe[
                        0 : min(len(reference_dataframe), 10000)
                    ].to_parquet(
                        path, allow_truncated_timestamps=True, engine="pyarrow"
                    )
            except (
                ValueError,
                NotImplementedError,
                KeyError,
                ParserError,
                OverflowError,
                TypeError,
                SyntaxError,
            ) as e:
                errors.append(
                    f"Your Dataframe could not be serialized to parquet. On attempting serialization, the "
                    f"following error was raised: {type(e).__name__}: {e} Serialization is required in order "
                    f"to ship your data to the Arthur platform. Please fix the data type issue and verify "
                    f"dataframe.to_parquet() succeeds."
                )

        # construct one error message for all validation errors found
        if len(errors) != 0:
            err_mess_init = f"{len(errors)} Validation Error(s): ["
            err_mess = "".join(
                f"ERROR {i + 1}: {errors[i]}, " for i in range(len(errors))
            )
            err_mess = err_mess_init + err_mess[: len(err_mess) - 2] + "]"
            raise UserTypeError(err_mess)

    def _retry_model_provisioning(self):
        self._client.post(
            f"/models/{self.id}/retry",
            return_raw_response=True,
            validation_response_code=HTTPStatus.OK,
        )
        self.await_model_ready()

    def _save_and_provision_model(self):
        self._check_model_valid()

        data = self.to_dict()
        data.pop("reference_dataframe", None)
        params = {
            "async_model_provisioning": True
        }  # setting request parameter for async model provisioning
        resp = self._client.post(
            "/models",
            json=data,
            params=params,
            return_raw_response=True,
            validation_response_code=HTTPStatus.CREATED,
        )
        resp_json = resp.json()
        if "id" not in resp_json:
            raise ExpectedParameterNotFoundError(
                f"An error occurred: {resp}, {resp.status_code}, {resp.content}"
            )

        logger.info(
            "We have registered the  model with Arthur and are getting it ready to accept inferences..."
        )

        # update fields with response from API
        self.id = resp_json["id"]
        self._store_model_id_in_env()

        if "status" in resp_json:  # For backward compatibility
            self.status = resp_json["status"]

        # Update Model Group associated fields
        if "model_group_id" in resp_json and "version_sequence_num" in resp_json:
            # Additional check above for backwards compatibility of SDK with previous versions of API
            if (
                self.model_group_id is not None
                and self.model_group_id != resp_json["model_group_id"]
            ):
                # Cannot update model group in MVP v1
                # TODO: Update in Model Versioning v2
                raise ArthurUnexpectedError(
                    "Model Group ID returned from model save does not match current not None MG ID."
                )
            self.model_group_id = resp_json["model_group_id"]
            self.version_sequence_num = resp_json["version_sequence_num"]

        # Add any new attributes and update existing attribute links
        for raw_attr in resp_json["attributes"]:
            new_attr = ArthurAttribute.from_dict(raw_attr)
            try:
                cur_attr = self.get_attribute(new_attr.name)
                cur_attr.attribute_link = new_attr.attribute_link
            except UserValueError:
                self._add_attribute_to_model(new_attr)

        # update classifier threshold
        if "classifier_threshold" in resp_json:
            self.classifier_threshold = resp_json["classifier_threshold"]

        if self.status is not None:  # None check for backward compatibility
            self.await_model_ready()

    def await_model_ready(self):
        """wait for model to be Ready

        Wait until the model reaches :py:attr:`~arthurai.common.constants.ModelStatus.Ready`
        or :py:attr:`~arthurai.common.constants.ModelStatus.CreationFailed` state. It also prints the log that a model
        is onboarding until a valid model state is reached.

        :raises ArthurUnexpectedError: If an exception occurs when checking the status of the model or model
            reaches :py:attr:`~arthurai.common.constants.ModelStatus.CreationFailed` state
        """

        if self.id is None:
            raise MethodNotApplicableError(
                "Cannot wait on an unregistered model. Please call save() method before "
                "trying to wait on the model to be ready"
            )
        self.status = ModelStatusWaiter(self, self._client).wait_for_valid_status(
            [ModelStatus.Ready, ModelStatus.CreationFailed],
            ONBOARDING_SPINNER_MESSAGE,
            ONBOARDING_UPDATE_MESSAGE,
        )

        if self.status == ModelStatus.Ready:
            logger.info(
                "Model Creation Completed successfully, you can now send Data to Arthur."
            )
        elif self.status == ModelStatus.CreationFailed:
            raise ArthurUnexpectedError(
                "Model Creation Failed. Please update your partner_model_id and retry to save "
                "the model or reach out to us at support@arthur.ai"
            )
        else:
            logger.info(
                f"Model Creation is in {self.status} state. Please make sure that the model status is Ready "
                f"by using await_model_ready() call before sending Data to Arthur"
            )

    def _check_model_valid(self) -> bool:
        """Check the validity of the model before saving, and prints out any errors it finds

        (As time passes we can add more to this function to enforce more requirements.)

        :return: True if the model is valid, False otherwise.
        """

        # has attributes
        if self.attributes is None:
            # future enhancement, attributes should be initialized to empty not None
            raise UnexpectedTypeError("attributes is None")
        if len(self.attributes) == 0:
            raise MissingParameterError(
                "must add attributes to model before saving; see below for requirements."
            )

        # contains ground truth, input, and predicted attributes
        contains_gt = False
        contains_pred = False
        contains_ipt = False
        for attr in self.attributes:
            if attr.stage == Stage.GroundTruth or attr.stage == Stage.GroundTruthClass:
                contains_gt = True
            if attr.stage == Stage.PredictedValue:
                contains_pred = True
            if (
                attr.stage == Stage.ModelPipelineInput
                or attr.stage == Stage.PredictFunctionInput
            ):
                contains_ipt = True
        if not contains_gt and self.output_type != OutputType.TokenSequence:
            raise MissingParameterError(
                "does not contain any attribute with Stage.GroundTruth."
            )
        if not contains_pred:
            raise MissingParameterError(
                "does not contain any attribute with Stage.PredictedValue."
            )
        if not contains_ipt:
            raise MissingParameterError(
                "does not have any attribute with Stage.ModelPipelineInput"
            )

        # for binary models, need one predicted attribute to be positive
        predicted_value_attributes = self.get_attributes(stage=Stage.PredictedValue)
        if (
            len(predicted_value_attributes) == 1
            and self.output_type == OutputType.Multiclass
        ):  # implicit binary model
            predicted_value_attributes[0].is_positive_predicted_attribute = True
        if (
            len(predicted_value_attributes) == 2
            and self.output_type == OutputType.Multiclass
        ):  # is binary model
            has_pos_pred = False
            for pred in predicted_value_attributes:
                if pred.is_positive_predicted_attribute:
                    has_pos_pred = True
            if not has_pos_pred:
                raise MethodNotApplicableError(
                    "binary models must have a positive predicted attribute; use "
                    "add_binary_classifier_output_attributes instead."
                )

        return True

    @arthur_excepted("failed to update model")
    def update(self):
        """Update the current model object in the Arthur platform

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: model write
        """
        if self.id is None:
            raise MethodNotApplicableError(
                "Model has not been created yet, use save() to instantiate this model object"
            )

        data = self.to_dict()
        resp = self._client.put(
            f"/models/{self.id}",
            json=data,
            return_raw_response=True,
            validation_response_code=HTTPStatus.OK,
        )

    @staticmethod
    def _get_attribute_data(
        value_type: ValueType, attribute_data_series: Series
    ) -> Dict:
        """Generates metadata about a specific attribute based on a supplied dataframe

        :param value_type:                          DataType of the values in the series
        :param attribute_data_series:              Pandas Series of data for the specific attribute
        :return: Dictionary of attribute metadata and values inferred from the pandas series
        """
        if attribute_data_series.isnull().any():
            raise UserValueError(
                "Column contains null value. Null values are not supported in reference or "
                f"inference data, please replace before proceeding."
            )

        if (
            value_type == ValueType.TimeSeries
        ):  # time series attrs should always be marked unique
            unique = True
            cnt_distinct = 0
        else:
            cnt_distinct = len(attribute_data_series.unique())
            unique = cnt_distinct == len(attribute_data_series) and cnt_distinct > 10
        attribute_data: Dict[str, Optional[Any]] = {"is_unique": unique}

        categorical = False
        if value_type == ValueType.Timestamp:
            categorical = False

        elif (
            value_type == ValueType.Float
            and 0 < cnt_distinct <= AUTO_CATEGORICAL_MAX
            and np.all(np.round(attribute_data_series) == attribute_data_series)
        ):  # all whole numbers
            categorical = True

        elif value_type == ValueType.Float:
            categorical = False
        elif value_type == ValueType.Integer and cnt_distinct <= 20:
            categorical = True
        elif value_type == ValueType.Integer:
            categorical = False
        elif value_type == ValueType.String:
            categorical = True
            if cnt_distinct > AUTO_CATEGORICAL_MAX:
                attribute_data["is_unique"] = True
        elif value_type == ValueType.Unstructured_Text:
            categorical = True
        elif value_type == ValueType.Image:
            categorical = False
        elif value_type == ValueType.TimeSeries:
            categorical = False
        else:
            categorical = True

        # even if unstructured text attributes aren't unique, we don't want categories
        if (
            categorical
            and not attribute_data["is_unique"]
            and not value_type == ValueType.Unstructured_Text
        ):
            attribute_frequency = attribute_data_series.value_counts()
            attribute_data["categories"] = [
                AttributeCategory(value=str(cat))
                for cat in list(attribute_frequency.index.values)
            ]
        # if not categorical, and numerical, set min/max
        elif not categorical and value_type in [
            ValueType.Float,
            ValueType.Integer,
            ValueType.Boolean,
        ]:
            attribute_data["min_range"] = core_util.NumpyEncoder.convert_value(
                attribute_data_series.min()
            )
            attribute_data["max_range"] = core_util.NumpyEncoder.convert_value(
                attribute_data_series.max()
            )

        attribute_data["categorical"] = categorical

        return attribute_data

    def _to_arthur_dtype(
        self, dtype: str, series: Series, stage: Stage
    ) -> Optional[ValueType]:
        """Select a :py:attr:`arthurai.common.constants.ValueType` based on a pandas dtype

        :param dtype: the pandas dtype
        :param series: the Series to infer values for
        :return: The :py:attr:`arthurai.common.constants.ValueType` corresponding to the pandas dtype
        """

        # in case of someone sending all nulls in a column, you can end up with empty series
        # handle example val of none, will not be able to distinguish between string or list, but should be edge case
        # and passing lists isn't expected, but we should handle most cases
        example_val = series.iloc[0] if len(series) > 0 else None

        if (
            dtype == "object"
            and (is_list_like(example_val) or example_val is None)
            and self.input_type == InputType.TimeSeries
            and stage == Stage.ModelPipelineInput
        ):
            return ValueType.TimeSeries
        elif dtype in ["string", "object"] and (
            isinstance(example_val, str) or example_val is None
        ):
            if self.input_type == InputType.Image and stage == Stage.ModelPipelineInput:
                return ValueType.Image
            else:
                return ValueType.String
        elif (
            dtype == "category"
        ):  # the pandas "category" dtype will fail the "isinstance" check above
            cat_dtype = series.dtype
            if isinstance(cat_dtype, CategoricalDtype):
                return self._to_arthur_dtype(
                    dtype=cat_dtype.categories.dtype.name, series=series, stage=stage
                )
            else:
                # should never happen but satisfies type checker
                raise TypeError(
                    f"Pandas dtype was 'categorical' but data type was not a pd.Categorical"
                )

        elif dtype in ["bool", "boolean"]:
            return ValueType.Boolean
        elif re.search("u?int*", dtype, flags=re.I) or re.search(
            "u?Int*", dtype, flags=re.I
        ):
            return ValueType.Integer
        elif re.search("float*", dtype, flags=re.I):
            return ValueType.Float
        elif re.search("(datetime|timestamp).*", dtype, flags=re.I):
            return ValueType.Timestamp
        else:
            return None

    def _get_pred_value_type(
        self, data: DataFrame, pred_to_ground_truth_map: Dict[str, str]
    ) -> ValueType:
        """
        Infer the Prediction Value Type for a Regression model based on a sample dataset and prediction to ground truth
        map.
        :param data:
        :param pred_to_ground_truth_map:
        :return:
        """
        if len(pred_to_ground_truth_map) == 0:
            raise UserValueError("pred_to_ground_truth_map cannot be empty")
        value_types = set()
        for col_name in pred_to_ground_truth_map.keys():
            cur_col = data[col_name]
            cur_value_type = self._to_arthur_dtype(
                cur_col.dtype.name, cur_col, stage=Stage.PredictedValue
            )
            if cur_value_type is None:
                raise UserValueError(
                    f"Cannot infer Arthur value type from Pandas dtype {cur_col.dtype.name} for "
                    f"column {col_name}"
                )
            value_types.add(cur_value_type)
        if len(value_types) > 1:
            raise UserValueError(
                f"Cannot have multiple prediction output columns with different datatypes! Got "
                f"types: {', '.join([str(v) for v in value_types])}"
            )

        return value_types.pop()

    @arthur_excepted("failed to parse dataframe")
    def from_dataframe(self, data: Union[DataFrame, Series], stage: Stage) -> None:
        """Auto-generate attributes based on input data

        .. deprecated:: 3.12.0
            Please use :func:`ArthurModel.infer_schema()` to add fields from a DataFrame to a model.

        Note that this does *not* automatically set reference
        data; this method only reads the passed-in data, and then infers attribute names, types, etc. and sets them up
        within the ArthurModel.

        .. seealso::
            To also set your data as reference data, see :func:`ArthurModel.build()`

        For PredictedValue and GroundTruth stages, use the correct `add_<modeltype>_output_attributes()` method instead.

        :param data: the data to infer attribute metadata from
        :param stage: :py:class:`.Stage` of the data
        :return: a DataFrame summarizing the inferred types
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        return self.infer_schema(data=data, stage=stage)

    @arthur_excepted("failed to infer schema from DataFrame")
    def infer_schema(self, data: Union[DataFrame, Series], stage: Stage) -> None:
        """Auto-generate attributes based on input data

        For an introduction to the model schema, see https://docs.arthur.ai/docs/preparing-for-onboarding#model-structure

        Note that this method does *not* automatically set reference
        data; this method only reads the passed-in data, and then infers attribute names, types, etc. and sets them up
        within the ArthurModel.

        .. seealso::
            To infer the model schema *and* set reference data in a single call, see :func:`ArthurModel.build()`.

            Once you've inferred the model schema with this function, you may want to set reference data separately
            with :func:`ArthurModel.set_reference_data()`.


        For PredictedValue and GroundTruth stages, use the correct `add_<modeltype>_output_attributes()` method instead.

        :param data: the data to infer attribute metadata from
        :param stage: :py:class:`.Stage` of the data
        :return: a DataFrame summarizing the inferred types
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """

        if (
            stage == Stage.PredictedValue
            or stage == Stage.GroundTruth
            or stage == Stage.GroundTruthClass
        ):
            raise MethodNotApplicableError(
                "Use either add_regression_output_attributes(), "
                "add_multiclass_classifier_output_attributes(), "
                "add_binary_classifier_output_attributes(), "
                "add_single_col_output_attributes(),  "
                "add_ranked_list_output_attributes(), "
                "or add_object_detection_output_attributes() to add output attributes."
            )

        if isinstance(data, DataFrame):
            df = data
        elif isinstance(data, Series):
            df = data.to_frame()
        else:
            raise UserTypeError(
                "Unsupported data type: a pandas.DataFrame or pandas.Series is required"
            )

        if len(df) == 0:
            raise UserValueError("Dataframe must have at least 1 row of data")

        found_categorical = False

        preferred_positions = self._generate_attr_positions(
            stage=stage, preferred_positions=list(range(len(df.columns)))
        )
        for i, column in enumerate(df.columns):
            try:
                series = core_util.standardize_pd_obj(
                    df[column],
                    dropna=True,
                    replacedatetime=False,
                    attributes=self.attributes_type_dict,
                )
                value_type = self._to_arthur_dtype(
                    series.dtype.name, series, stage=stage
                )
                # handle unknown datatype
                if value_type is None:
                    logger.warning(
                        f"Cannot parse type {series.dtype.name} for column {column}. Not including in schema. "
                        f"Valid types are: str, int, float, datetime, timestamp, bool, time series. To manually add an "
                        f"attribute use model.add_attribute(). Run help(model.add_attribute) for full "
                        f"documentation."
                    )
                    continue

                attribute_data = self._get_attribute_data(value_type, series)
            except ArthurUserError as e:
                raise type(e)(f"Error in column '{column}': {str(e)}") from e

            if value_type == ValueType.String and self.input_type == InputType.NLP:
                value_type = ValueType.Unstructured_Text
                # even if unstructured text attributes are not unique we don't want to store categories
                attribute_data["categories"] = None

            if value_type == ValueType.Image:
                # even if image attributes are not unique we don't want to store categories
                attribute_data["categories"] = None

            if (
                attribute_data["categorical"]
                and value_type != ValueType.Unstructured_Text
            ):
                found_categorical = True

            attribute_data["position"] = preferred_positions[i]
            arthur_attribute = ArthurAttribute(
                name=column, stage=stage, value_type=value_type, **attribute_data
            )
            self._add_attribute_to_model(arthur_attribute)
        if found_categorical:
            logger.warning(
                f"Found one or more categorical attributes. It is suggested to use model.review() to "
                "verify all possible categories were inferred correctly for each categorical attribute. "
                "To update with new categories, use model.get_attribute(attr_name).set(categories=[cat_1, "
                "cat_2, cat_3])"
            )

    def build_token_sequence_model(
        self,
        input_column: Union[str, List[str]],
        output_text_column: str,
        input_token_column: Optional[str] = None,
        output_token_column: Optional[str] = None,
        output_likelihood_column: Optional[str] = None,
        ground_truth_text_column: Optional[str] = None,
        ground_truth_tokens_column: Optional[str] = None,
        data: Optional[DataFrame] = None,
    ) -> DataFrame:
        if self.input_type not in [InputType.Tabular, InputType.TimeSeries]:
            if isinstance(input_column, list):
                raise ValueError(
                    "Only tabular or time series models may specify multiple input columns"
                )
            if data is not None:
                logger.warning(
                    "Data was supplied by model with an input type that is not tabular or time series. "
                    "Not using data frame to build model"
                )

        # build input attrs
        if self.input_type == InputType.NLP:
            input_text_attr = _text_attr(input_column, stage=Stage.ModelPipelineInput)
            if input_token_column:
                input_token_attr = _tokens_attr(
                    name=input_token_column, stage=Stage.PredictFunctionInput
                )
                # link attributes
                input_token_attr.token_attribute_link = input_text_attr.name
                input_text_attr.token_attribute_link = input_token_attr.name
                self._add_attribute_to_model(input_token_attr)
            self._add_attribute_to_model(input_text_attr)

        elif self.input_type == InputType.Image:
            input_image_attr = _image_attr(input_column)
            self._add_attribute_to_model(input_image_attr)
        elif self.input_type in [InputType.Tabular, InputType.TimeSeries]:
            if data is not None:
                self.infer_schema(
                    data=data[input_column], stage=Stage.ModelPipelineInput
                )

        # build predicted value attributes
        output_text_attr = _text_attr(output_text_column, stage=Stage.PredictedValue)
        position = 1
        if output_token_column:
            output_token_attr = _tokens_attr(
                name=output_token_column, stage=Stage.PredictedValue, position=position
            )
            position += 1
            # link attributes
            output_text_attr.token_attribute_link = output_token_attr.name
            output_token_attr.token_attribute_link = output_text_attr.name
            self._add_attribute_to_model(output_token_attr)
        if output_likelihood_column:
            output_likelihood_attr = _token_likelihoods_attr(
                output_likelihood_column, position=position
            )
            # link attributes if not already linked
            if output_text_attr.token_attribute_link is None:
                output_text_attr.token_attribute_link = output_likelihood_attr.name
                output_likelihood_attr.token_attribute_link = output_text_attr.name
            self._add_attribute_to_model(output_likelihood_attr)
        self._add_attribute_to_model(output_text_attr)

        # build ground truth attrs
        if ground_truth_text_column:
            gt_text_attr = _text_attr(
                name=ground_truth_text_column, stage=Stage.GroundTruth
            )
            if ground_truth_tokens_column:
                gt_tokens_attr = _tokens_attr(
                    name=ground_truth_tokens_column, stage=Stage.GroundTruth, position=1
                )
                # link attributes
                gt_tokens_attr.token_attribute_link = gt_text_attr.name
                gt_text_attr.token_attribute_link = gt_tokens_attr.name
                self._add_attribute_to_model(gt_tokens_attr)
            self._add_attribute_to_model(gt_text_attr)

        return self.review()

    def build(
        self,
        data: DataFrame,
        pred_to_ground_truth_map: Dict[str, Any],
        positive_predicted_attr: Optional[str] = None,
        non_input_columns: Optional[List[str]] = None,
        ground_truth_column: Optional[str] = None,
        set_reference_data=True,
    ) -> DataFrame:
        """
        Build an Arthur model from a Pandas DataFrame,
        inferring the attribute metadata and registering the reference data to be stored with Arthur.

        For a quickstart guide to building an ArthurModel, see https://docs.arthur.ai/docs/quickstart

        The `pred_to_ground_truth_map` parameter tells Arthur how the predicted value attributes
        relate to the ground truth attributes of your model.

        This dictionary can be formatted two different ways:

        1) a prediction column name to ground truth column name mapping passed to pred_to_ground_truth_map

        .. code-block:: python

            # map PredictedValue attribute to its corresponding GroundTruth attribute
            # this tells Arthur that the `pred_value` column represents
            # the predicted value corresponding to the
            # ground truth values in the `gt_column` column
            PRED_TO_GROUND_TRUTH_MAP = {'pred_value' : 'gt_column'}

            arthur_model.build(reference_df,
                               pred_to_ground_truth_map=PRED_TO_GROUND_TRUTH_MAP)

        2) a prediction column name to ground truth class value mapping passed to pred_to_ground_truth_map,
                plus the name of the column holding the ground truth class values passed to ground_truth_column

        .. code-block:: python

            # map PredictedValue attribute to its corresponding GroundTruth attribute value
            # this tells Arthur that the `pred_value` column represents
            # the probability that the GroundTruth attribute `gt_column` = 1
            # which we indicate in arthur_model.build() with the `ground_truth_column` parameter
            PRED_TO_GROUND_TRUTH_MAP = {'pred_value' : 1}

            arthur_model.build(reference_df,
                               ground_truth_column="gt_column",
                               pred_to_ground_truth_map=PRED_TO_GROUND_TRUTH_MAP)

        Note that this function will remove any previously existing attributes. Combines calls to
        :func:`ArthurModel.infer_schema()` and (if `set_reference_data` is True)
        :func:`ArthurModel.set_reference_data()`

        :param data: a reference DataFrame to build the model from
        :param pred_to_ground_truth_map: a mapping from predicted column names to their corresponding ground truth
            column names, or ground truth values in ground_truth_column
        :param positive_predicted_attr: name of the predicted attribute to register as the positive predicted
            attribute
        :param non_input_columns: list of columns that contain auxiliary data not directly passed into the model
        :param set_reference_data: if True, register the provided DataFrame as the model's reference dataset
        :param ground_truth_column: a single column name containing ground truth labels.
            must be used with pred to ground truth class map

        :return: a DataFrame summarizing the inferred types
        """
        if non_input_columns is None:
            non_input_columns = []

        if self.model_is_saved():
            raise MethodNotApplicableError("Model is already built and saved!")

        # clear current attributes
        self.attributes = []
        ground_truth_columns = (
            [ground_truth_column]
            if ground_truth_column
            else list(pred_to_ground_truth_map.values())
        )
        pred_columns = [
            pred for pred in pred_to_ground_truth_map.keys() if pred is not None
        ]
        if len(pred_columns) == 0:
            raise UserValueError(
                f"'pred_to_ground_truth_map' must specify at least one predicted attribute"
            )

        # if all ground truth columns are missing in the data, suggest using 'ground_truth_column'
        # if some are found, but others are missing, just say some are missing
        missing_gt_cols = [c for c in ground_truth_columns if c not in data.columns]
        if 0 < len(missing_gt_cols) == len(ground_truth_columns):
            raise UserValueError(
                f"No Ground Truth columns: '{missing_gt_cols}' not found in DataFrame. If using a "
                f"single ground truth column with class labels, make sure to set the "
                f"'ground_truth_column' parameter."
            )
        elif 0 < len(missing_gt_cols) < len(ground_truth_columns):
            raise UserValueError(
                f"Some Ground Truth columns: '{missing_gt_cols}' not found in DataFrame."
            )

        # do some initial validation to ensure columns exist
        missing_pred_cols = [c for c in pred_columns if c not in data.columns]
        missing_non_input_cols = [c for c in non_input_columns if c not in data.columns]
        if len(missing_pred_cols) > 0 or len(missing_non_input_cols) > 0:
            err = "Missing columns in the DataFrame."
            if len(missing_pred_cols) > 0:
                err += f" Predicted Value columns {missing_pred_cols} not found."
            if len(missing_non_input_cols) > 0:
                err += f" Non Input columns {missing_non_input_cols} not found."
            raise UserValueError(err)

        # validate attribute names are formatted correctly
        validate_attr_names(data.columns)

        if ground_truth_column:
            # if using ground truth column, mapping values must be in the column
            ground_truth_values = data[ground_truth_column].unique()
            for val in pred_to_ground_truth_map.values():
                if val not in ground_truth_values:
                    raise UserValueError(
                        f"{val} not in {ground_truth_column} of DataFrame. "
                        f"When using ground_truth_column, pred_to_ground_truth_map must contain "
                        f"values in the ground truth column "
                    )
        else:
            # otherwise, mapping values should be columns
            for col in pred_to_ground_truth_map.values():
                if col not in data.columns:
                    raise UserValueError(f"Ground truth column {col} not in DataFrame.")

        # infer schema, filtering out prediction and ground truth columns
        input_cols = [
            col
            for col in data.columns
            if (col not in ground_truth_columns)
            and (col not in pred_columns)
            and (col not in non_input_columns)
        ]
        self.infer_schema(data=data[input_cols], stage=Stage.ModelPipelineInput)
        self.infer_schema(data=data[non_input_columns], stage=Stage.NonInputData)

        # validate schema based on model input type
        if self.input_type == InputType.TimeSeries:
            self._validate_time_series_model_schema()

        # add prediction and ground truth columns
        if self.output_type == OutputType.Multiclass:
            if len(data[pred_columns].select_dtypes(exclude="float").columns):
                raise UserTypeError(
                    f"Predicted values for classification models should be floats representing "
                    f"predicted probabilities. Please redefine columns "
                    f"{data[pred_columns].select_dtypes(exclude='float').columns.to_list()} as floats."
                )

            if len(pred_to_ground_truth_map) <= 2:
                if positive_predicted_attr is None:
                    if (
                        len(pred_columns) == 1
                    ):  # implicitly set pos class when using single col pred
                        positive_predicted_attr = pred_columns[0]
                    else:
                        raise UserTypeError(
                            f"Binary Classifiers require 'positive_predicted_attr' parameter. Please "
                            f"add this parameter (possible values: '{pred_columns[0]}' or "
                            f"'{pred_columns[1]}')"
                        )
            if ground_truth_column:
                self.add_classifier_output_attributes_gtclass(
                    pred_to_ground_truth_class_map=pred_to_ground_truth_map,
                    ground_truth_column=ground_truth_column,
                    data=data,
                    positive_predicted_attr=positive_predicted_attr,
                )
            else:
                if len(pred_to_ground_truth_map) < 2:
                    raise UserValueError(
                        f"Classification models require 2 or more predicted attributes. Currently, only "
                        f"{len(pred_to_ground_truth_map)} is specified: {list(pred_to_ground_truth_map.keys())}. "
                        f"Arthur requires a column that contains the probability of each predicted class."
                    )
                elif len(pred_to_ground_truth_map) == 2:
                    if self.classifier_threshold is not None:
                        self.add_binary_classifier_output_attributes(
                            positive_predicted_attr=positive_predicted_attr,
                            pred_to_ground_truth_map=pred_to_ground_truth_map,
                            threshold=self.classifier_threshold,
                        )
                    else:
                        self.add_binary_classifier_output_attributes(
                            positive_predicted_attr=positive_predicted_attr,
                            pred_to_ground_truth_map=pred_to_ground_truth_map,
                        )
                else:
                    self.add_multiclass_classifier_output_attributes(
                        pred_to_ground_truth_map=pred_to_ground_truth_map
                    )
        elif self.output_type == OutputType.Regression:
            pred_value_type = self._get_pred_value_type(data, pred_to_ground_truth_map)
            self.add_regression_output_attributes(
                data=data,
                pred_to_ground_truth_map=pred_to_ground_truth_map,
                value_type=pred_value_type,
            )
        elif self.output_type == OutputType.RankedList:
            if len(pred_columns) != 1 or len(ground_truth_columns) != 1:
                raise UserValueError(
                    f"Ranked List models require 1 predicted attribute and 1 ground truth attribute. "
                    f"Currently, {len(pred_columns)} predicted attributes are specified and "
                    f"{len(ground_truth_columns)} ground truth attributes are specified."
                )
            else:
                self.add_ranked_list_output_attributes(
                    predicted_attr_name=pred_columns[0],
                    gt_attr_name=ground_truth_columns[0],
                )
                self._validate_ranked_list_model(data=data)
        else:
            # future enhancement: make this method work for object detection models
            #  this will require accepting output class labels, which is generally a decent thing to do but is probably
            #  best included with adding multilabel support to not pollute our API with CV-specific parameters
            raise MethodNotApplicableError(
                f"Cannot use build() method for models with output type {self.output_type}"
            )

        # set reference data
        if set_reference_data:
            self.set_reference_data(data=data)

        # review
        logger.info(
            "Please review the inferred schema. If everything looks correct, lock in your model by calling "
            "arthur_model.save()"
        )
        return self.review()

    def _add_attribute_to_model(self, attribute: ArthurAttribute) -> ArthurAttribute:
        """Adds an already-made ArthurAttribute to the model.

        :param attribute: ArthurAttribute Object to add to the model
        :return: ArthurAttribute Object
        """
        if self.attributes is None:
            self.attributes = [attribute]
        else:
            self.attributes.append(attribute)

        self.attributes_type_dict[attribute.name] = attribute.value_type

        return attribute

    def _generate_attr_positions(
        self, stage: Stage, preferred_positions: List[int]
    ) -> List[int]:
        """
        Given a list of preferred attribute positions, generate actual positions if the preferred indices are not
        available in the current stage
        :param stage:
        :param preferred_positions:
        :return:
        """
        cur_attr_positions = set()
        if self.attributes is not None:
            for attr in self.attributes:
                if attr.stage == stage and attr.position is not None:
                    cur_attr_positions.add(attr.position)

        actual_positions = []
        for pref_pos in preferred_positions:
            if pref_pos not in cur_attr_positions:
                position = pref_pos
            else:
                position = max(cur_attr_positions) + 1
            actual_positions.append(position)
            cur_attr_positions.add(position)
        return actual_positions

    def _validate_ranked_list_model(self, data: DataFrame) -> None:
        """Validates ranked list model schema and reference dataset

        Validates ranked list model predicted and ground truth attributes have supported metadata and value types and
        the reference dataset meets maximum size restrictions: max 100 recommendations per inference and max 1000 total
        unique recommended items. Doesn't support reference dataset datatype validation.

        :raises: UserValueError: Error was found during validation.
        """
        # validate there is only one ground truth attribute & one predicted attribute
        pred_attrs = self.get_attributes(stage=Stage.PredictedValue)
        gt_attrs = self.get_attributes(stage=Stage.GroundTruth)
        if len(pred_attrs) != 1:
            raise UserValueError(
                f"Ranked List models must have exactly one predicted attribute. Your model has "
                f"{len(pred_attrs)} predicted attributes."
            )
        else:
            pred_attr = pred_attrs[0]
        if len(gt_attrs) != 1:
            raise UserValueError(
                f"Ranked List models must have exactly one ground truth attribute. Your model has "
                f"{len(gt_attrs)} ground truth attributes."
            )
        else:
            gt_attr = gt_attrs[0]

        # validate gt & pred attr have correct value types and are not categorical
        if pred_attr.value_type != ValueType.RankedList:
            raise UserValueError(
                f"The Ranked List model predicted attribute must be of value type "
                f"{ValueType.RankedList}. Your predicted attribute {pred_attr.name} has value type "
                f"{pred_attr.value_type}"
            )
        elif gt_attr.value_type != ValueType.StringArray:
            raise UserValueError(
                f"The Ranked List model ground truth attribute must be of value type "
                f"{ValueType.StringArray}. Your ground truth attribute {gt_attr.name} has value type "
                f"{gt_attr.value_type}"
            )
        elif pred_attr.categorical:
            raise UserValueError(
                f"The Ranked List model predicted attribute {pred_attr.name} cannot be categorical."
            )
        elif gt_attr.categorical:
            raise UserValueError(
                f"The Ranked List model ground truth attribute {gt_attr.name} cannot be categorical."
            )

        # validate recommendation data size limits
        if data is not None:
            if pred_attr.name not in data.columns:
                raise UserValueError(
                    f"The provided dataset does not have a column for the predicted attribute: "
                    f"{pred_attr.name}"
                )
            elif gt_attr.name not in data.columns:
                raise UserValueError(
                    f"The provided dataset does not have a column for the ground truth attribute: "
                    f"{gt_attr.name}"
                )

            # enforce 100 recommendations per inference limit
            pred_gt_df = data[[gt_attr.name, pred_attr.name]]
            rec_count_per_inf_df = pred_gt_df.applymap(
                lambda x: len(x) > 100 if is_list_like(x) else None
            )
            if rec_count_per_inf_df.any(axis=None):
                raise UserValueError(
                    f"Each inference in a Ranked List model can have a maximum of 100 recommendations "
                    f"per inference. At least one inference had more than 100 recommendations in "
                    f"either the ground truth column {gt_attr.name} or the predicted value column "
                    f"{pred_attr.name}."
                )

            # enforce 1000 total unique recommended items limit
            unique_gt_values = (
                pred_gt_df[gt_attr.name]
                .explode()
                .apply(lambda x: x if is_str_like(x) else None)
            )
            unique_pred_values = (
                pred_gt_df[pred_attr.name]
                .explode()
                .apply(lambda x: dict(x).get("item_id") if valid_rec_obj(x) else None)
            )
            unique_recs = set(unique_gt_values.dropna()) | set(
                unique_pred_values.dropna()
            )
            if len(unique_recs) > 1000:
                raise UserValueError(
                    f"A Ranked List model can have a maximum of 1000 total unique recommended items "
                    f"in its ground truth and predicted value columns. Your model has "
                    f"{len(unique_recs)} total recommended items across attributes {pred_attr.name} "
                    f"and {gt_attr.name}."
                )

    def _validate_time_series_model_schema(self) -> None:
        """Validates model schema for time series input type model

        Confirms that a time series input type model has at least one Time Series value type attribute in the
        ModelPipelineInput stage and that attribute is not categorical

        :raises UserValueError: Found issue with model schema
        :raises MethodNotApplicableError: Model is not a time series input type model
        """
        if self.input_type != InputType.TimeSeries:
            raise MethodNotApplicableError(
                "model is not a time series input type model"
            )

        found_time_series = False
        if self.attributes is not None:
            for attr in self.attributes:
                if (
                    attr.stage == Stage.ModelPipelineInput
                    and attr.value_type == ValueType.TimeSeries
                ):
                    if attr.categorical:
                        raise UserValueError(
                            "Time Series value type attributes cannot be categorical."
                        )
                    found_time_series = True
                    break
        if not found_time_series:
            raise UserValueError(
                "Time Series input type models must have at least one time series type PIPELINE_INPUT "
                "attribute with data formatted as lists of dicts with 'timestamp' and 'value' keys."
            )

    @arthur_excepted("failed to remove attribute")
    def remove_attribute(
        self,
        name: Optional[str] = None,
        stage: Optional[Stage] = None,
        attribute: Optional[ArthurAttribute] = None,
    ) -> None:
        """Removes an already-made ArthurAttribute from the model.

        Note that attributes may only be removed from unsaved models - for a saved model, attributes are immutable.

        :param name: Optional string, the name of the ArthurAttribute Object to remove from the model
        :param stage: Optional Stage, the stage of the ArthurAttribute Object to remove from the model
        :param attribute: Optional ArthurAttribute Object to remove from the model
        :return: None
        :raises MethodNotApplicableError: failed due to incorrect usage on saved model
        :raises UserValueError: failed due to user error inputting unrecognized attribute
        """
        if self.model_is_saved():
            raise MethodNotApplicableError(
                "attributes cannot be removed from a saved model"
            )

        if self.attributes:
            for a in self.attributes:
                if name and a.name == name:
                    _attr = self.get_attribute(name, stage)
                    self.attributes.remove(_attr)
                    return None
                if attribute and a == attribute:
                    self.attributes.remove(attribute)
                    return None
            raise UserValueError(
                "The attribute you have provided does not exist in the ArthurModel"
            )
        else:
            raise UserValueError("The ArthurModel has no attributes")

    @arthur_excepted("failed to add attribute")
    def add_attribute(
        self,
        name: Optional[str] = None,
        value_type: Optional[ValueType] = None,
        stage: Optional[Stage] = None,
        label: Optional[str] = None,
        position: Optional[int] = None,
        categorical: bool = False,
        min_range: Optional[Union[float, int]] = None,
        max_range: Optional[Union[float, int]] = None,
        monitor_for_bias: bool = False,
        categories: Optional[List[Union[str, AttributeCategory]]] = None,
        bins: Optional[List[Union[NumberType, AttributeBin]]] = None,
        is_unique: bool = False,
        is_positive_predicted_attribute: bool = False,
        attribute_link: Optional[str] = None,
        arthur_attribute: Optional[ArthurAttribute] = None,
        gt_pred_attrs_map: Optional[Dict] = None,
    ) -> List[ArthurAttribute]:
        """Adds a new attribute of stage ModelPipelineInput or NonInputData to the model.

        For an introduction to attributes and stages, see https://docs.arthur.ai/user-guide/basic_concepts.html#attributes-and-stages

        If you have built your model using arthur_model.build(), your model attributes may already be inferred and you
        do not need to add them with this function.

        Formatting requirement: attribute names must contain only letters, numbers, and underscores, and cannot begin
        with a number.

        .. code-block:: python

            from arthurai.common.constants import Stage, ValueType

            # adds a float input attribute directly to the model
            arthur_model.add_attribute(
                name="attribute_name",
                value_type=ValueType.Float,
                stage=Stage.ModelPipelineInput
            )

        This method can be used to add any attribute to your Arthur model and configure its properties. For some specific
        model types and data types, it can be more convenient to use a method for adding model attributes from this table:

        .. list-table:: Adding Model Attributes
           :widths: 70 10 10 10
           :header-rows: 1

           * - Method
             - InputType
             - OutputType
             - Stage
           * - :func:`ArthurModel.add_attribute()`
             - Any
             - Any
             - Any
           * - :func:`ArthurModel.add_binary_classifier_output_attributes()`
             - Any
             - Binary
             - PredictedValue and GroundTruth
           * - :func:`ArthurModel.add_classifier_output_attributes_gtclass()`
             - Any
             - Multiclass
             - PredictedValue and GroundTruthClass
           * - :func:`ArthurModel.add_multiclass_classifier_output_attributes()`
             - Any
             - Multiclass
             - PredictedValue and GroundTruth
           * - :func:`ArthurModel.add_regression_output_attributes()`
             - Any
             - Regression
             - PredictedValue and GroundTruth
           * - :func:`ArthurModel.add_image_attribute()`
             - Image
             - Any
             - ModelPipelineInput
           * - :func:`ArthurModel.add_object_detection_output_attributes()`
             - Image
             - ObjectDetection
             - PredictedValue and GroundTruth


        :param attribute_link: Only applicable for `GroundTruth` or `PredictedValue` staged attributes.
            If stage is equal to `GroundTruth`, this represents the associated `PredictedValue` attribute and vice versa
        :param is_positive_predicted_attribute: Only applicable for `PredictedValue` attributes on a Binary
            Classification model. Should be set to `True` on the positive predicted value attribute.
        :param is_unique: Boolean value used to signal if the values of this attribute are unique.
        :param bins: List of bin cut-offs used to discretize continuous attributes. Use `None` as an open ended value.
            ``[None, 18, 65, None]`` represents the three following bins: ``value < 18, 18 < value < 65, value > 65``
        :param monitor_for_bias: boolean value set to `True` if the attribute should be monitored for bias
        :param max_range: Max value for a continuous attribute
        :param min_range: Min value for a continuous attribute
        :param categorical: Boolean value set to `True` if the attribute has categorical values.
        :param position: The array position of attribute within the stage. Required in the PREDICT_FUNCTION_INPUT stage.
        :param label: Label for attribute. If attribute has an encoded name, a more readable label can be set.
        :param stage: :class:`arthurai.common.constants.Stage` of this attribute in the model pipeline
        :param value_type: :class:`arthurai.common.constants.ValueType` associated with this attributes values
        :param name: Name of the attribute. Attribute names can only contain alpha-numeric characters and underscores
            and cannot start with a number.
        :param categories: [Only for Categorical Attributes] If the attribute is categorical, this will contain the
            attribute's categories. It is required only if the categorical flag is set to true.
        :param arthur_attribute: Optional ArthurAttribute to add to the model
        :param gt_pred_attrs_map:

            .. deprecated:: version 2.0.0

                Use `ArthurModel.add_[model_type]_output_attributes()` instead

        :return: ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        if arthur_attribute is None:
            if stage is None or value_type is None or name is None:
                raise MissingParameterError(
                    "At minimum stage, value_type, and name must be provided for an attribute"
                )
            elif (
                stage == Stage.PredictedValue
                or stage == Stage.GroundTruth
                or gt_pred_attrs_map is not None
            ):
                raise MethodNotApplicableError(
                    "Use either add_regression_output_attributes(), "
                    "add_multiclass_classifier_output_attributes(), "
                    "add_ranked_list_output_attributes(), "
                    "or add_binary_classifier_output_attributes() to add output attributes."
                )

            if not self._validate_attribute_name(name):
                raise UserValueError(
                    "Invalid attribute name: must contain only numbers, letters, and underscores, "
                    "and cannot start with a number."
                )

            # Add categories or bins if supplied
            attribute_categories = (
                [
                    (
                        AttributeCategory(value=c)
                        if not isinstance(c, AttributeCategory)
                        else c
                    )
                    for c in categories
                ]
                if categories
                else None
            )

            attribute_bins: Optional[List[Any]] = None
            if bins and not isinstance(bins[0], AttributeBin):
                attribute_bins = [
                    AttributeBin(bins[i], bins[i + 1]) for i in range(len(bins) - 1)
                ]
            elif bins and isinstance(bins[0], AttributeBin):
                attribute_bins = bins

            attribute_to_add = ArthurAttribute(
                name=name,
                value_type=value_type,
                stage=stage,
                label=label,
                position=position,
                categorical=categorical,
                min_range=min_range,
                max_range=max_range,
                monitor_for_bias=monitor_for_bias,
                categories=attribute_categories,
                bins=attribute_bins,
                is_unique=is_unique,
                is_positive_predicted_attribute=is_positive_predicted_attribute,
                attribute_link=attribute_link,
            )
            return [self._add_attribute_to_model(attribute_to_add)]

        else:
            self._validate_attribute_name(arthur_attribute.name)
            return [self._add_attribute_to_model(arthur_attribute)]

    @arthur_excepted("failed to add image attribute")
    def add_image_attribute(self, name: Optional[str] = None) -> List[ArthurAttribute]:
        """Wraps add_attribute for images (see :func:`ArthurModel.add_attribute()`)

        Automatically sets the stage as ModelPipelineInput

        :return: ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """

        position = self._generate_attr_positions(
            Stage.ModelPipelineInput, preferred_positions=[0]
        )[0]
        return self.add_attribute(
            name=name,
            stage=Stage.ModelPipelineInput,
            value_type=ValueType.Image,
            categorical=False,
            is_unique=True,
            position=position,
        )

    @arthur_excepted("failed to fetch image")
    def get_image(
        self,
        image_id: str,
        save_path: str,
        type: ImageResponseType = ImageResponseType.RawImage,
    ) -> str:
        """Saves the image specified by image_id to a file

        :param image_id: id of image in model
        :param save_path: directory to save the downloaded image to
        :param type: type of response data

        :return: location of downloaded image file
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data read
        """

        endpoint = f"/models/{self.id}/inferences/images/{image_id}"
        resp = self._client.get(
            endpoint, params={"type": type}, return_raw_response=True
        )

        # validate success response without specifying exact status code because it involves a redirect
        validation.validate_response_status(
            response_or_code=resp.status_code, allow_redirects=True
        )

        content_type = resp.headers["Content-Type"]
        file_ext = IMAGE_FILE_EXTENSION_MAP.get(content_type, "")
        save_file = f"{save_path}/{type}_{image_id}{file_ext}"

        with open(save_file, "wb") as file:
            file.write(resp.content)

        return save_file

    @arthur_excepted("failed to find image attribute")
    def get_image_attribute(self) -> ArthurAttribute:
        """Returns the attribute with value_type=Image for input_type=Image models

        :return: ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        if self.attributes is None:
            raise UserValueError("No attributes have been defined on this model")

        for attr in self.attributes:
            if attr.value_type == ValueType.Image:
                return attr

        raise UserValueError("No attribute with value_type Image found")

    @staticmethod
    def _validate_attribute_name(attribute_name: str) -> bool:
        """Checks that attribute name is valid.

        :param attribute_name: name of the attribute to add to the model
        :return: boolean indicating whether the name is valid.
        """

        if bool(re.compile("\d").search(attribute_name[0])):  # \d is all the digits 0-9
            print("Attribute name cannot start with a number.")
            return False

        if bool(
            re.compile("\W").search(attribute_name)
        ):  # \W is the complement of all alphanumeric characters and _.
            print("Attribute name can only contain numbers, letters, and underscores.")
            return False

        return True

    @arthur_excepted("failed to add regression output attributes")
    def add_regression_output_attributes(
        self,
        pred_to_ground_truth_map: Dict[str, str],
        value_type: ValueType,
        data: Optional[DataFrame] = None,
    ) -> Dict[str, ArthurAttribute]:
        """Registers ground truth attributes and predicted value attributes for regression models.

        For an introduction to attributes and stages, see https://docs.arthur.ai/user-guide/basic_concepts.html#attributes-and-stages

        .. code-block:: python

            from arthurai.common.constants import ValueType

            # map PredictedValue attributes to their corresponding GroundTruth attributes
            PRED_TO_GROUND_TRUTH_MAP = {
                "pred_value": "gt_value",
            }

            # add the ground truth and predicted attributes to the model
            arthur_model.add_regression_output_attributes(
                pred_to_ground_truth_map = PRED_TO_GROUND_TRUTH_MAP,
                value_type = ValueType.Float
            )

        :param pred_to_ground_truth_map: Map of predicted value attributes to their corresponding ground truth attribute names.
                                  The names provided in the dictionary will be used to register the one-hot encoded
                                  version of the attributes.
        :param value_type: Value type of regression model output attribute (usually either ValueType.Integer or ValueType.Float)
        :param data: a reference DataFrame to build the model from. This is optional since it is currently only used
                    to calculate the min_range and max_range values of the predicted + ground truth attributes. If data
                    is not passed, min_range and max_range are not set in the attributes

        :return: Mapping of added attributes string name -> ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        attributes_added = {}

        preferred_positions = list(range(len(pred_to_ground_truth_map)))
        pred_attr_positions = self._generate_attr_positions(
            Stage.PredictedValue, preferred_positions
        )
        gt_attr_positions = self._generate_attr_positions(
            Stage.GroundTruth, preferred_positions
        )
        i = 0
        for pred_attr, gt_attr in pred_to_ground_truth_map.items():
            arthur_gt_attr = ArthurAttribute(
                name=gt_attr,
                stage=Stage.GroundTruth,
                value_type=value_type,
                categorical=False,
                attribute_link=pred_attr,
                position=gt_attr_positions[i],
            )
            arthur_pred_attr = ArthurAttribute(
                name=pred_attr,
                stage=Stage.PredictedValue,
                value_type=value_type,
                categorical=False,
                attribute_link=gt_attr,
                position=pred_attr_positions[i],
            )

            # Since min_range and max_range fields are conditional on passing of data, they are set
            # post attribute creation using set() function on the condition that data != None
            if data is not None:
                gt_ranges = {
                    "min_range": core_util.NumpyEncoder.convert_value(
                        data[gt_attr].min()
                    ),
                    "max_range": core_util.NumpyEncoder.convert_value(
                        data[gt_attr].max()
                    ),
                }
                pred_ranges = {
                    "min_range": core_util.NumpyEncoder.convert_value(
                        data[pred_attr].min()
                    ),
                    "max_range": core_util.NumpyEncoder.convert_value(
                        data[pred_attr].max()
                    ),
                }
                arthur_gt_attr.set(**gt_ranges)
                arthur_pred_attr.set(**pred_ranges)

            self._add_attribute_to_model(arthur_gt_attr)
            self._add_attribute_to_model(arthur_pred_attr)
            attributes_added[arthur_pred_attr.name] = arthur_pred_attr
            attributes_added[arthur_gt_attr.name] = arthur_gt_attr
            i += 1
        return attributes_added

    @arthur_excepted("failed to add output attributes")
    def add_classifier_output_attributes_gtclass(
        self,
        pred_to_ground_truth_class_map: Dict[str, Any],
        ground_truth_column: str,
        data: DataFrame,
        positive_predicted_attr: Optional[str] = None,
    ) -> Dict[str, ArthurAttribute]:
        """Registers ground truth and predicted value attributes for classification models

        Registers a GroundTruthClass attribute. In addition, registers a predicted value attribute for each of the
        model's predicted values.

        For an introduction to attributes and stages,
        see https://docs.arthur.ai/user-guide/basic_concepts.html#attributes-and-stages

        Create a predicted value attribute for each key in pred_to_ground_truth_class_map and a ground truth class
        attribute for the ground_truth_column.

        .. code-block:: python

            # Map PredictedValue attribute to its corresponding GroundTruth attribute value.
            # This tells Arthur that the `pred_survived` column represents
            # the probability that the ground truth column has the value 1
            PRED_TO_GROUND_TRUTH_MAP = {
                "pred_value": 1
            }

            # Add the ground truth and predicted attributes to the model,
            # specifying which attribute represents ground truth and
            # which attribute represents the predicted value.
            arthur_model.add_classifier_output_attributes_gtclass(
                positive_predicted_attr = 'pred_value',
                pred_to_ground_truth_class_map = PRED_TO_GROUND_TRUTH_MAP,
                ground_truth_column = 'gt_column'
            )

        :param pred_to_ground_truth_class_map: map from predicted column names to corresponding ground truth values
        :param ground_truth_column: column name of column in data holding the ground truth values
        :param data: DataFrame containing ground truth column data
        :param positive_predicted_attr: string name of the predicted attribute to register as the positive predicted
               attribute, if binary classification

        return: Mapping of added attributes string name -> ArthurAttribute Object
        """
        attributes_added = {}
        gt_class_value_type = self._to_arthur_dtype(
            data[ground_truth_column].dtype.name,
            data[ground_truth_column],
            Stage.GroundTruthClass,
        )
        if gt_class_value_type not in [ValueType.String, ValueType.Integer]:
            raise ArthurUserError(
                f"Ground Truth Class column data must be of type string or type integer."
                f" Received type {gt_class_value_type}"
            )

        gt_class_attr_dict = self._get_attribute_data(
            gt_class_value_type, data[ground_truth_column]
        )

        gt_class_attr = ArthurAttribute(
            name=ground_truth_column,
            stage=Stage.GroundTruthClass,
            value_type=gt_class_value_type,
            position=0,
            **gt_class_attr_dict,
        )
        self._add_attribute_to_model(gt_class_attr)
        attributes_added[ground_truth_column] = gt_class_attr

        #####
        # here, we generate attribute positions based on the number of attributes
        # if there is only one attribute, we set its position to 1
        # (so that the negative class attribute can have position 0 to match with other integrations e.g. Sagemaker)
        num_pred_values = len(pred_to_ground_truth_class_map)
        if num_pred_values == 1:
            pred_attr_positions = [1]
        else:
            preferred_positions = list(range(num_pred_values))
            pred_attr_positions = self._generate_attr_positions(
                Stage.PredictedValue, preferred_positions
            )
        #####

        for i, pred_attr in enumerate(pred_to_ground_truth_class_map.keys()):
            is_pos_pred_attr = True if positive_predicted_attr == pred_attr else False
            arthur_pred_attr = ArthurAttribute(
                name=pred_attr,
                stage=Stage.PredictedValue,
                value_type=ValueType.Float,
                min_range=0,
                max_range=1,
                position=pred_attr_positions[i],
                is_positive_predicted_attribute=is_pos_pred_attr,
                # this is required for linking of implicit attributes
                gt_class_link=str(pred_to_ground_truth_class_map[pred_attr]),
            )
            self._add_attribute_to_model(arthur_pred_attr)
            attributes_added[arthur_pred_attr.name] = arthur_pred_attr
        return attributes_added

    @arthur_excepted("failed to add output attributes")
    def add_multiclass_classifier_output_attributes(
        self, pred_to_ground_truth_map: Dict[str, str]
    ) -> Dict[str, ArthurAttribute]:
        """Registers GroundTruth and PredictedValue attributes

        For an introduction to attributes and stages,
        see https://docs.arthur.ai/user-guide/basic_concepts.html#attributes-and-stages

        This function will create a predicted value and
        ground truth attribute for each mapping specified in pred_to_ground_truth_map.

        .. code-block:: python

            # map PredictedValue attributes to their corresponding GroundTruth attributes
            PRED_TO_GROUND_TRUTH_MAP = {
                "dog": "dog_gt",
                "cat": "cat_gt",
                "horse": "horse_gt"
            }

            # add the ground truth and predicted attributes to the model
            arthur_model.add_multiclass_classifier_output_attributes(
                pred_to_ground_truth_map = PRED_TO_GROUND_TRUTH_MAP
            )

        :param pred_to_ground_truth_map: Map of predicted value attributes to their corresponding ground truth attribute names.
                                  The names provided in the dictionary will be used to register the one-hot encoded
                                  version of the attributes. Ensure the ordering of items in this dictionary is an accurate
                                  representation of how model predictions (probability vectors) will be generated.
        :return: Mapping of added attributes string name -> ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """

        if len(pred_to_ground_truth_map) <= 2:
            raise UserValueError(
                f"`add_multiclass_classifier_output_attributes` requires more than 2 predicted attributes. Currently, "
                f"only {len(pred_to_ground_truth_map)} are specified: {list(pred_to_ground_truth_map.keys())}. "
                f"Arthur requires a column that contains the probability of each predicted class. You can use the "
                f"`add_binary_classifier_output_attributes` method to onboard a binary classification model."
            )

        preferred_positions = list(range(len(pred_to_ground_truth_map)))
        pred_attr_positions = self._generate_attr_positions(
            Stage.PredictedValue, preferred_positions
        )
        gt_attr_positions = self._generate_attr_positions(
            Stage.GroundTruth, preferred_positions
        )

        attributes_added = {}
        for i, (pred_attr, gt_attr) in enumerate(pred_to_ground_truth_map.items()):
            arthur_gt_attr = ArthurAttribute(
                name=gt_attr,
                stage=Stage.GroundTruth,
                value_type=ValueType.Integer,
                categorical=True,
                categories=[AttributeCategory(value="0"), AttributeCategory(value="1")],
                attribute_link=pred_attr,
                position=gt_attr_positions[i],
            )
            arthur_pred_attr = ArthurAttribute(
                name=pred_attr,
                stage=Stage.PredictedValue,
                value_type=ValueType.Float,
                min_range=0,
                max_range=1,
                attribute_link=gt_attr,
                position=pred_attr_positions[i],
            )
            self._add_attribute_to_model(arthur_gt_attr)
            self._add_attribute_to_model(arthur_pred_attr)
            attributes_added[arthur_pred_attr.name] = arthur_pred_attr
            attributes_added[arthur_gt_attr.name] = arthur_gt_attr
        return attributes_added

    @arthur_excepted("failed to add output attributes")
    def add_binary_classifier_output_attributes(
        self,
        positive_predicted_attr: str,
        pred_to_ground_truth_map: Dict[str, str],
        threshold: float = 0.5,
    ) -> Dict[str, ArthurAttribute]:
        """Registers GroundTruth and PredictedValue attributes and their thresholds

        For an introduction to attributes and stages,
        see https://docs.arthur.ai/user-guide/basic_concepts.html#attributes-and-stages

        This function will create a predicted value and ground truth attribute for each mapping specified in
        pred_to_ground_truth_map.

        .. code-block:: python

            # map PredictedValue attributes to their corresponding GroundTruth attributes
            PRED_TO_GROUND_TRUTH_MAP = {'pred_0' : 'gt_0',
                                        'pred_1' : 'gt_1'}

            # add the ground truth and predicted attributes to the model
            # specifying that the `pred_1` attribute is the
            # positive predicted attribute, which means it corresponds to the
            # probability that the binary target attribute is 1
            arthur_model.add_binary_classifier_output_attributes(positive_predicted_attr='pred_1',
                                                                 pred_to_ground_truth_map=PRED_TO_GROUND_TRUTH_MAP)


        For binary models, `GroundTruth` is always an integer, and `PredictedAttribute` is always a float.
        Additionally, `PredictedAttribute` is expected to be a probability (e.g. the output of a scikit-learn
        model's `predict_proba` method), rather than a classification to 0/1.

        This assumes that separate columns for predicted values and ground truth values have already been created,
        and that they have both been broken into two separate (pseudo-onehot) columns: for example, the column
        `ground_truth_label` becomes `ground_truth_label=0` and `ground_truth_label=1`, and the column `pred_prob`
        becomes `pred_prob=0` and `pred_prob=1`. The pandas function `pd.get_dummies()` can be useful for reformatting
        the ground truth column, but be sure that the datatype is specified correctly as an int.

        :param positive_predicted_attr: string name of the predicted attribute to register as the positive predicted attribute
        :param pred_to_ground_truth_map: Map of predicted value attributes to their corresponding ground truth attribute names.
                                  The names provided in the dictionary will be used to register the one-hot encoded
                                  version of the attributes. For example: `{'pred_0': 'gt_0', 'pred_1': 'gt_1'}`,
                                  Ensure the ordering of items in this dictionary is an accurate
                                  representation of how model predictions (probability vectors) will be generated.
        :param threshold: Threshold to use for the classifier model, defaults to 0.5

        :return: Mapping of added attributes string name -> ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        if len(pred_to_ground_truth_map) != 2:
            raise UserValueError(
                (
                    f"Binary classifiers must have two output attributes, but pred_to_ground_truth_map "
                    f"has {len(pred_to_ground_truth_map)}. To add more than two output attributes to a "
                    f"multiclass model, use add_multiclass_classifier_output_attributes()."
                )
            )
        if positive_predicted_attr not in pred_to_ground_truth_map.keys():
            raise UserValueError(
                (
                    f"The positive_predicted_attr must be included in the mapping "
                    f"pred_to_ground_truth_map. positive_predicted_attr {positive_predicted_attr} not "
                    f"found in pred_to_ground_truth_map keys: {pred_to_ground_truth_map.keys()}."
                )
            )
        preferred_pred_positions = list(
            range(
                len(
                    [
                        pred
                        for pred in pred_to_ground_truth_map.keys()
                        if pred is not None
                    ]
                )
            )
        )
        preferred_gt_positions = list(
            range(
                len([gt for gt in pred_to_ground_truth_map.values() if gt is not None])
            )
        )
        pred_attr_positions = self._generate_attr_positions(
            Stage.PredictedValue, preferred_pred_positions
        )
        gt_attr_positions = self._generate_attr_positions(
            Stage.GroundTruth, preferred_gt_positions
        )
        attributes_added = {}
        next_pred_pos_idx = 0
        next_gt_pos_idx = 0
        for pred_attr_name, gt_attr_name in pred_to_ground_truth_map.items():
            is_pos_pred_attr = positive_predicted_attr == pred_attr_name
            if pred_attr_name is not None:
                arthur_pred_attr = ArthurAttribute(
                    name=pred_attr_name,
                    stage=Stage.PredictedValue,
                    value_type=ValueType.Float,
                    min_range=0,
                    max_range=1,
                    attribute_link=gt_attr_name,
                    is_positive_predicted_attribute=is_pos_pred_attr,
                    position=pred_attr_positions[next_pred_pos_idx],
                )
                self._add_attribute_to_model(arthur_pred_attr)
                attributes_added[arthur_pred_attr.name] = arthur_pred_attr
                next_pred_pos_idx += 1

            if gt_attr_name is not None:
                arthur_gt_attr = ArthurAttribute(
                    name=gt_attr_name,
                    stage=Stage.GroundTruth,
                    value_type=ValueType.Integer,
                    categorical=True,
                    categories=[
                        AttributeCategory(value="0"),
                        AttributeCategory(value="1"),
                    ],
                    attribute_link=pred_attr_name,
                    position=gt_attr_positions[next_gt_pos_idx],
                )
                self._add_attribute_to_model(arthur_gt_attr)
                attributes_added[arthur_gt_attr.name] = arthur_gt_attr
                next_gt_pos_idx += 1

        self.classifier_threshold = threshold
        return attributes_added

    @arthur_excepted("failed to add output attributes")
    def add_object_detection_output_attributes(
        self, predicted_attr_name: str, gt_attr_name: str, image_class_labels: List[str]
    ) -> Dict[str, ArthurAttribute]:
        """Registers ground truth and predicted value attributes for an object detection model, as well as
        setting the image class labels.

        For a guide to onboarding object detection models,
        see https://docs.arthur.ai/user-guide/walkthroughs/cv_onboarding.html#object-detection

        This function will create a predicted value attribute and ground truth attribute using the names provided,
        giving each a value type of Bounding Box. Image class labels are also set on the model object. The index
        of each label in the list should correspond to a class_id the model outputs.

        Ex: image_class_labels = ['cat', 'dog', 'person']
        So a bounding box with class_id of 0 would have label 'cat',
        class_id of 1 would have label 'dog', and class_id of 2 would have label 'person'

        .. code-block:: python

            predicted_attribute_name = "objects_detected"
            ground_truth_attribute_name = "label"
            class_labels = ['cat', 'dog', 'person']

            arthur_model.add_object_detection_output_attributes(
                predicted_attribute_name,
                ground_truth_attribute_name,
                class_labels)

        :param predicted_attr_name: The name of the predicted value attribute
        :param gt_attr_name: The name of the ground truth attribute
        :param image_class_labels: The labels for each class the model can predict, ordered by their class_id

        :return: Mapping of added attributes string name -> ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        if predicted_attr_name == gt_attr_name:
            raise UserValueError(
                "Predicted value attribute name matched ground truth attribute name. Attribute names "
                "must be unique"
            )
        if len(image_class_labels) == 0:
            raise UserValueError("Must provide at least one class label")
        if (
            self.input_type != InputType.Image
            or self.output_type != OutputType.ObjectDetection
        ):
            raise MethodNotApplicableError(
                "This function can only be called for models with Image input and Object "
                "Detection output"
            )

        arthur_gt_attr = ArthurAttribute(
            name=gt_attr_name,
            stage=Stage.GroundTruth,
            value_type=ValueType.BoundingBox,
            attribute_link=predicted_attr_name,
            position=self._generate_attr_positions(
                Stage.GroundTruth, preferred_positions=[0]
            )[0],
        )
        arthur_pred_attr = ArthurAttribute(
            name=predicted_attr_name,
            stage=Stage.PredictedValue,
            value_type=ValueType.BoundingBox,
            attribute_link=gt_attr_name,
            position=self._generate_attr_positions(
                Stage.PredictedValue, preferred_positions=[0]
            )[0],
        )
        self._add_attribute_to_model(arthur_gt_attr)
        self._add_attribute_to_model(arthur_pred_attr)
        self.image_class_labels = image_class_labels

        return {predicted_attr_name: arthur_pred_attr, gt_attr_name: arthur_gt_attr}

    @arthur_excepted("failed to add output attributes")
    def add_ranked_list_output_attributes(
        self, predicted_attr_name: str, gt_attr_name: str
    ) -> Dict[str, ArthurAttribute]:
        """Registers ground truth and predicted value attributes for a ranked list model.

        This function will create a predicted value attribute and ground truth attribute using the names provided.
        The predicted value attribute will have a Ranked List value type and the ground truth attribute will have
        a String Array value type.

        .. code-block:: python

            predicted_attribute_name = "ranked_recommendations"
            ground_truth_attribute_name = "liked_items"

            arthur_model.add_ranked_list_output_attributes(
                predicted_attribute_name,
                ground_truth_attribute_name)

        :param predicted_attr_name: The name of the predicted value attribute
        :param gt_attr_name: The name of the ground truth attribute

        :return: Mapping of added attributes string name -> ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        if predicted_attr_name == gt_attr_name:
            raise UserValueError(
                "Predicted value attribute name matched ground truth attribute name. Attribute names "
                "must be unique."
            )
        elif self.output_type != OutputType.RankedList:
            raise MethodNotApplicableError(
                "This function can only be called for models with Ranked List output."
            )

        arthur_gt_attr = ArthurAttribute(
            name=gt_attr_name,
            stage=Stage.GroundTruth,
            value_type=ValueType.StringArray,
            attribute_link=predicted_attr_name,
            position=0,
        )
        arthur_pred_attr = ArthurAttribute(
            name=predicted_attr_name,
            stage=Stage.PredictedValue,
            value_type=ValueType.RankedList,
            attribute_link=gt_attr_name,
            position=0,
        )
        self._add_attribute_to_model(arthur_gt_attr)
        self._add_attribute_to_model(arthur_pred_attr)
        return {predicted_attr_name: arthur_pred_attr, gt_attr_name: arthur_gt_attr}

    @arthur_excepted("failed to swap predicted attribute positions")
    def swap_predicted_attribute_positions(self, persist_if_saved=True):
        """Swap the position of the model's two predicted attributes

        This function should be used when enabling explainability:
        in particular, if your model's predict function requires attributes
        in a specific order, but the attribute positions have not yet been inferred correctly.

        :param persist_if_saved: if the model has been saved, call update() to persist the change
        :return:
        """
        predicted_attrs = self.get_attributes(stage=Stage.PredictedValue)
        if len(predicted_attrs) != 2:
            raise MethodNotApplicableError(
                f"Model must have exactly two predicted attributes to swap their positions"
            )

        pos_0 = predicted_attrs[0].position
        predicted_attrs[0].position = predicted_attrs[1].position
        predicted_attrs[1].position = pos_0

        if self.model_is_saved() and persist_if_saved:
            self.update()

    @arthur_excepted("failed to get attribute")
    def get_attribute(
        self, name: str, stage: Optional[Stage] = None
    ) -> ArthurAttribute:
        """Retrieves an attribute by name and stage

        :param name: string name of the attribute to retrieve
        :param stage: Optional `Stage` of attribute to retrieve

        :return: ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        if self.attributes is None:
            raise MethodNotApplicableError("model does not have any attributes")
        for attr in self.attributes:
            if attr.name == name and (stage is None or attr.stage == stage):
                return attr

        raise UserValueError(
            f"Attribute with name: {name} in stage: {stage} does not exist"
        )

    @arthur_excepted("failed to get attributes")
    def get_attributes(self, stage: Optional[Stage] = None) -> List[ArthurAttribute]:
        """Returns a list of attributes for the specified stage. If stage is not supplied the function will return
        all attributes.

        :param stage: :class:`arthurai.common.constants.Stage` to filter by
        :return: List of :class:`arthurai.attributes.ArthurAttribute`
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        if self.attributes is None:
            return []
        if stage is None:
            return [attr for attr in self.attributes]
        else:
            return [attr for attr in self.attributes if attr.stage == stage]

    @arthur_excepted("failed to get attribute names")
    def get_attribute_names(
        self, stage: Optional[Stage] = None, value_type: Optional[ValueType] = None
    ) -> List[str]:
        """
        Returns a list of the names of attributes for the specified stage and/or value type. If both stage and value
        type are not supplied the function will return all attribute names.

        :param stage: :class:`arthurai.common.constants.Stage` to filter by
        :param value_type: :class:`arthurai.common.constants.ValueType` to filter by
        :return: List of string attribute names
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        if self.attributes is None:
            raise MethodNotApplicableError("model does not have any attributes")
        if stage is None and value_type is None:
            return [attr.name for attr in self.attributes]
        elif stage is not None and value_type is not None:
            return [
                attr.name
                for attr in self.attributes
                if attr.stage == stage and attr.value_type == value_type
            ]
        elif stage is None:
            return [
                attr.name for attr in self.attributes if attr.value_type == value_type
            ]
        else:
            return [attr.name for attr in self.attributes if attr.stage == stage]

    @arthur_excepted("failed to rename attribute")
    def rename_attribute(
        self, old_name: str, new_name: str, stage: Stage
    ) -> ArthurAttribute:
        """Renames an attribute by name and stage

        :param old_name: string name of the attribute to rename
        :param new_name: string new name of the attribute
        :param stage: `Stage` of attribute

        :return: ArthurAttribute Object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        attribute = self.get_attribute(old_name, stage)
        attribute.name = new_name

        return attribute

    @arthur_excepted("failed to set attribute labels")
    def set_attribute_labels(
        self,
        attribute_name: str,
        labels: Dict[Union[int, str], str],
        attribute_stage: Optional[Stage] = None,
    ):
        """
        Sets labels for individual categories of a specific attribute

        This function should be used to set the labels corresponding to the
        different possible values that an attribute can take.

        .. code-block:: python

            # labels the value 0 for the attribute 'education_level'
            # to have the label 'elementary', etc.
            arthur_model.set_attribute_labels(
                'education_level',
                {0 : 'elementary', 1 : 'middle', 2 : 'high', 3 : 'university'}
            )


        :param attribute_name: Attribute name to set the categories labels
        :param attribute_stage: Optional stage of the attribute which is being updated
        :param labels: Dictionary where the key is the categorical value and the value is the string categorical label
        :return: None
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        attr_to_update = self.get_attribute(name=attribute_name, stage=attribute_stage)
        categories = []
        for cat_value, cat_label in labels.items():
            categories.append(AttributeCategory(value=cat_value, label=cat_label))
        attr_to_update.categories = categories

    @arthur_excepted("failed to generate summary")
    def review(
        self, stage: Stage = None, props: Optional[List[str]] = None, print_df=False
    ) -> Optional[DataFrame]:
        """Prints a summary of the properties of all attributes in the model.

        :param stage: restrict the output to a particular :py:class:`.Stage` (defaults to all stages)
        :param props: a list of properties to display in the summary
                   valid properties are data_type, categorical, is_unique,
                   categories, cutoffs, range, monitor_for_bias, position
                   (defaults to data_type, categorical, is_unique)
        :param print_df: boolean value whether to print df or return it, defaults to False

        :return: a DataFrame summarizing the inferred types; or None if `print_df` is True
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """

        if props is None:
            props = [
                "value_type",
                "categorical",
                "is_unique",
                "categories",
                "bins",
                "range",
                "monitor_for_bias",
            ]

        attributes: Optional[List[ArthurAttribute]] = None
        if stage is None:
            attributes = self.attributes
            display_items = ["name", "stage"] + props
        else:
            attributes = self.get_attributes(stage=stage)
            display_items = ["name"] + props
        if attributes is None:
            raise MissingParameterError("model does not have any attributes")

        result_df = DataFrame(columns=display_items, dtype=object)

        for attribute in attributes:
            row: Dict[str, Union[str, List[str]]] = {}
            for item in display_items:
                if item == "range":
                    row[item] = f"[{attribute.min_range}, {attribute.max_range}]"
                elif item == "categories":
                    string_categories = []
                    categories = (
                        [] if attribute.categories is None else attribute.categories
                    )
                    for cat in categories:
                        if cat.label is not None:
                            string_categories.append(
                                "{" + f"label: {cat.label}, value: {cat.value}" + "}"
                            )
                        else:
                            string_categories.append("{" + f"value: {cat.value}" + "}")
                    row[item] = string_categories
                else:
                    row[item] = attribute.__getattribute__(item)
            result_df = result_df.append(row, ignore_index=True)

        if print_df:
            try:
                display(result_df)  # type: ignore
            except NameError:
                print(result_df)
            return None
        else:
            return result_df

    @arthur_excepted("failed to set predict function input order")
    def set_predict_function_input_order(self, attributes: List[str]) -> None:
        """Sets the expected order of attributes used by the prediction function.

        This function should be used when enabling explainability:
        in particular, if your model's predict function requires attributes
        in a specific order, but the attribute positions have not yet been inferred correctly.

        :param attributes: a list of attribute names

        :return: None
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        for idx, name in enumerate(attributes):
            attribute = self.get_attribute(name, Stage.ModelPipelineInput)
            attribute.position = idx

    @arthur_excepted("failed to set attribute as sensitive")
    def set_attribute_as_sensitive(
        self, attribute_name: str, attribute_stage: Optional[Stage] = None
    ) -> None:
        """Sets the passed-in attribute to be sensitive by setting `attr.monitor_for_bias` = True.

        You will need to call `self.save()` or `self.update()` after this method; we do not
        automatically call the API in this method.

        :param attribute_name: Name of attribute to set as sensitive.
        :param attribute_stage: Stage of attribute to set as sensitive.

        :return: None

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        attribute = self.get_attribute(attribute_name, attribute_stage)

        attribute.monitor_for_bias = True

    @arthur_excepted("failed to enable explainability")
    def enable_explainability(
        self,
        df: Optional[DataFrame] = None,
        project_directory: Optional[str] = None,
        user_predict_function_import_path: Optional[str] = None,
        streaming_explainability_enabled: Optional[bool] = True,
        requirements_file: str = "requirements.txt",
        python_version: Optional[str] = None,
        sdk_version: str = __version__,
        model_server_num_cpu: Optional[str] = None,
        model_server_memory: Optional[str] = None,
        model_server_max_replicas: Optional[int] = None,
        inference_consumer_num_cpu: Optional[str] = None,
        inference_consumer_memory: Optional[str] = None,
        inference_consumer_thread_pool_size: Optional[int] = None,
        inference_consumer_score_percent: Optional[float] = None,
        explanation_nsamples: Optional[int] = None,
        explanation_algo: Optional[str] = None,
        ignore_dirs: Optional[List[str]] = None,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Enable explainability for this model.

        :param df: a dataframe containing the :py:class:`.Stage.ModelPipelineInput` values for this model. Required
            for non-image models.
        :param project_directory: the name of the directory containing the model source code. Required.
        :param user_predict_function_import_path: the name of the file that implements or wraps the predict function.
            Required.
        :param streaming_explainability_enabled: Defaults to true. flag to turn on streaming explanations which will
            explain every inference sent to the platform. If false, explanations will need to be manually generated for
            each inference via the Arthur API. Set to false if worried about compute cost.
        :param requirements_file: the name of the file that contains the pip requirements (default: requirements.txt)
        :param python_version: the python version (default: sys.version). Should be in the form of <major>.<minor>
        :param sdk_version: the version of the sdk to initialize the model servier with
        :param model_server_num_cpu: string number of CPUs to provide to model server docker container. If not
            provided, 1 CPU is used. Specified in the format of Kubernetes CPU resources. '1', '1.5', '100m', etc.
        :param model_server_memory: The amount of memory to allocate to the model server docker container. Provided
            in the format of kubernetes memory resources "1Gi" or "500Mi" (default: None).
        :param model_server_max_replicas: The max number of model servers to create
        :param inference_consumer_num_cpu: string number of CPUs to provide to inference consumer docker container.
            If not provided, 1 CPU is used. Specified in the format of Kubernetes CPU resources. '1', '1.5', '100m',
            etc. (default: '1')
        :param inference_consumer_memory: The amount of memory to allocate to the model server docker container.
            Provided in the format of kubernetes memory resources "1Gi" or "500Mi" (default: '1G').
        :param inference_consumer_thread_pool_size: The number of inference consumer workers, this determines how
            many requests to the model server can be made in parallel. Default of 5. If increasing, CPU should be
            increased as well.
        :param inference_consumer_score_percent: What percent of inferences should get scored. Should be a value
            between 0.0 and 1.0. Default 1.0 (everything is scored)
        :param explanation_nsamples: number of predictions to use in the explanation. For SHAP and LIME, the default is
            2000. (default: None)
        :param explanation_algo: the algorithm to use for explaining inferences. Valid values are 'lime' and 'shap'.
            Defaults to 'lime'.
        :param ignore_dirs: a list of directories within the project_directory that you do not want to include when
            uploading the model.  Path is relative to project_directory.
        :return: response content
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: enrichment_config write
        """
        if self.input_type == InputType.NLP and self.text_delimiter is None:
            raise MissingParameterError(
                "Must set a text delimiter for NLP models prior to enabling explainability"
            )
        if python_version is None:
            python_version = f"{sys.version_info[0]}.{sys.version_info[1]}"
            if sys.version_info[0] == 3 and sys.version_info[1] >= 9:
                raise UserValueError(
                    "Explainability not supported for Python 3.9 and greater. Please use Python 3.8"
                )
        if self.input_type != InputType.Image and df is None:
            raise MissingParameterError(
                "Must provide example dataframe for NLP and Tabular models"
            )
        if project_directory is None:
            raise MissingParameterError("project_directory must be specified")
        if user_predict_function_import_path is None:
            raise MissingParameterError(
                "user_predict_function_import_path must be specified"
            )
        if df is not None and len(df) < 5000:
            logger.warning(
                f"Only pasing {len(df)} rows into explainer. The explanation algorithm uses this example "
                f"data to generate distributions  in order to perturb data and generate explanations. This "
                f"example data should be representative of your training set. Ideally this data should "
                f"contain examples of all possible categorical values, and wide range of possible "
                f"continuous attributes. If desired, rerun this function with more data passed to update "
                f"the explainer."
            )

        explainability_config = dict(
            df=df,
            project_directory=project_directory,
            ignore_dirs=ignore_dirs if ignore_dirs else [],
            user_predict_function_import_path=user_predict_function_import_path,
            streaming_explainability_enabled=streaming_explainability_enabled,
            requirements_file=requirements_file,
            python_version=python_version,
            sdk_version=sdk_version,
            explanation_nsamples=explanation_nsamples,
            explanation_algo=explanation_algo,
            model_server_num_cpu=model_server_num_cpu,
            model_server_memory=model_server_memory,
            model_server_max_replicas=model_server_max_replicas,
            inference_consumer_num_cpu=inference_consumer_num_cpu,
            inference_consumer_memory=inference_consumer_memory,
            inference_consumer_thread_pool_size=inference_consumer_thread_pool_size,
            inference_consumer_score_percent=inference_consumer_score_percent,
            seed=seed,
        )
        return self.update_enrichment(
            Enrichment.Explainability, True, explainability_config
        )

    @arthur_excepted("failed to enable bias mitigation")
    def enable_bias_mitigation(self):
        """Updates the bias mitigation Enrichment to be enabled

        .. seealso::
            This convenience function wraps :func:`ArthurModel.update_enrichment()`

        :permissions: enrichment_config write
        """

        self._check_model_save()

        if not self.check_has_bias_attrs():
            raise MethodNotApplicableError(
                "This model has no attributes marked as monitor for bias."
            )
        if not self.get_positive_predicted_class():
            raise MethodNotApplicableError(
                "Bias mitigation is currently only supported for binary classifiers."
            )

        return self.update_enrichment(Enrichment.BiasMitigation, True, config=None)

    def model_is_saved(self) -> bool:
        """Returns True if and only if the model has been saved to the Arthur platform"""
        return self.id is not None

    def _check_model_save(self, msg="You must save the model before sending"):
        if not self.model_is_saved():
            raise MethodNotApplicableError(msg)

    def _store_model_id_in_env(self):
        """
        This environment variable allows callers to retrieve created model IDs without capturing the return
        value of the save() or get_model() Python calls, e.g. for integration tests to fetch created model
        IDs and archive them in the parent process.
        """
        if self.id is not None:
            os.environ["ARTHUR_LAST_MODEL_ID"] = self.id

    def _attempt_close_batches(
        self, complete_batch: bool, batch_counts: Dict[str, int]
    ) -> None:
        if self.is_batch and complete_batch:
            for batch_id, batch_count in batch_counts.items():
                self.close_batch(batch_id, batch_count)

    @arthur_excepted("failed to send inferences")
    def send_inferences(
        self,
        inferences: Union[List[Dict[str, Any]], Dict[str, List[Any]], DataFrame],
        predictions: Optional[
            Union[List[Dict[str, Any]], Dict[str, List[Any]], DataFrame, Sequence[Any]]
        ] = None,
        inference_timestamps: Optional[Sequence[Union[datetime, str]]] = None,
        ground_truths: Optional[
            Union[List[Dict[str, Any]], Dict[str, List[Any]], DataFrame, Sequence[Any]]
        ] = None,
        ground_truth_timestamps: Optional[Sequence[Union[datetime, str]]] = None,
        tz: Optional[str] = None,
        partner_inference_ids: Optional[Sequence[str]] = None,
        batch_id: Optional[str] = None,
        fail_silently: bool = False,
        complete_batch: bool = True,
        wait_for_enrichments: bool = False,
    ):
        # TODO [OBS-563]: we are setting wait_for_enrichments to False by default, but we plan on setting it to True
        #  after February 1, 2024
        """
        Send inferences to the Arthur API. The `inferences` parameter may contain all the inference data, or only the
        input data if predictions and metadata are supplied separately. At a minimum, input data and predictions should
        be passed in: `partner_inference_id`, `inference_timestamp`, and (if ground truth data is supplied)
        `ground_truth_timestamp` fields are required by the Arthur API, but these will be generated if not supplied.

        .. seealso::
            To send large amounts of data or Parquet/json files, see :func:`ArthurModel.send_bulk_inferences()`

        **Examples:**

        An input dataframe and predicted probabilities array, leaving the partner inference IDs and timestamps to be
        auto-generated:

        .. code-block:: python

            input_df = pd.DataFrame({"input_attr": [2]})
            pred_array = my_sklearn_model.predict_proba(input_df)
            arthur_model.send_inferences(input_df, predictions=pred_array, batch_id='batch1')

        All data in the inferences parameter in the format expected by the
        `Arthur API POST Inferences Endpoint
        <https://docs.arthur.ai/api-documentation/v3-api-docs.html#tag/inferences/paths/
        ~1models~1{model_id}~1inferences/post>`_:

        .. code-block:: python

            inference_data = [
                {
                    "inference_timestamp": "2021-06-16T16:52:11Z",
                    "partner_inference_id": "inf1",
                    "batch_id": "batch1",
                    "inference_data": {
                        "input_attr": 2,
                        "predicted_attr": 0.6
                    },
                    "ground_truth_timestamp": "2021-06-16T16:53:45Z",
                    "ground_truth_data": {
                        "ground_truth_attr": 1
                    }
                }
            ]
            arthur_model.send_inferences(inference_data)

        A list of dicts without nested `inference_data` or `ground_truth` fields:

        .. code-block:: python

            inference_data = [
                {
                    "inference_timestamp": "2021-06-16T16:52:11Z",
                    "partner_inference_id": "inf1",
                    "batch_id": "batch1",
                    "input_attr": 2,
                    "predicted_attr": 0.6,
                    "ground_truth_timestamp": "2021-06-16T16:53:45Z",
                    "ground_truth_attr": 1
                }
            ]
            arthur_model.send_inferences(inference_data)


        :param inferences: inference data to send, containing at least input values and optionally predictions, ground
         truth, timestamps, partner inference ids, and batch IDs.
        :param predictions: the model predictions, in a table-like format for one or more columns or a list-like format
         if the model has only one predicted column. overwrites any predictions supplied in the `inferences` parameter
        :param inference_timestamps: the inference timestamps, in a list-like format as ISO-8601 strings or datetime
         objects. if no timestamps are supplied in `inferences` or this parameter, they will be generated from the
         current time. overwrites any timestamps in the `inferences` parameter.
        :param ground_truths: the optional ground truth data (true labels), in a table-like format for one or more
         columns or a list-like format if the model has only one ground truth column. overwrites any ground truth values
         supplied in the `inferences` parameter
        :param ground_truth_timestamps: the ground truth timestamps, in a list-like format as ISO-8601 strings or
         datetime objects. if no ground truth timestamps are supplied in `inferences` or this parameter but ground truth
         data is supplied, they will be generated from the current time. overwrites any timestamps in the `inferences`
         parameter.
        :param tz: datetime timezone object or timezone string
        :param partner_inference_ids: partner_inference_ids to be attached to these inferences, which can be used to
         send ground truth data later or retrieve specific inferences, in a list-like format containing strings. if no
         partner_inference_ids are supplied in `inference` or this parameter, they will be auto-generated.
        :param batch_id: a single batch ID to use for all inferences supplied. overwrites any batch IDs in the
         `inferences` parameter
        :param fail_silently: if True, log failed inferences but do not raise an exception
        :param complete_batch: if True, mark all batches in this dataset as completed
        :param wait_for_enrichments: if True, wait until all the model enrichments are in a ready state before sending
         inferences. Defaults to False.

        :return: Upload status response in the following format:

         .. code-block:: python

            {
              "counts": {
                "success": 1,
                "failure": 0,
                "total": 1
              },
              "results": [
                {
                  "partner_inference_id" "inf-id",
                  "message": "success",
                  "status": 200
                }
              ]
            }

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data write
        """
        self._check_model_save(msg="Must save model before sending inferences.")

        if wait_for_enrichments:
            await_enrichments_ready(self)

        # add separately provided parameters and reformat inferences to nested list of dicts
        inferences = self._format_inferences(
            inferences,
            True,  # format_timestamps
            predictions,
            inference_timestamps,
            ground_truths,
            ground_truth_timestamps,
            tz,
            partner_inference_ids,
        )

        # add missing data
        added_inference_timestamps = 0
        added_gt_timestamps = 0
        added_partner_inference_ids = 0
        sent_partner_inference_ids = []
        batch_counts: Dict[str, int] = {}
        current_iso_timestamp = datetime.now(pytz.utc).isoformat()
        for i in range(len(inferences)):
            if "inference_timestamp" not in inferences[i].keys():
                inferences[i]["inference_timestamp"] = current_iso_timestamp
                added_inference_timestamps += 1
            if "ground_truth_data" in inferences[i].keys():
                if "ground_truth_timestamp" not in inferences[i]:
                    inferences[i]["ground_truth_timestamp"] = current_iso_timestamp
                    added_gt_timestamps += 1
            if batch_id is not None:
                inferences[i]["batch_id"] = batch_id
            if "partner_inference_id" not in inferences[i].keys():
                inferences[i]["partner_inference_id"] = shortuuid.uuid()
                added_partner_inference_ids += 1
            if self.is_batch and "batch_id" in inferences[i].keys():
                batch_counts[inferences[i]["batch_id"]] = (
                    batch_counts.get(inferences[i]["batch_id"], 0) + 1
                )
            sent_partner_inference_ids.append(inferences[i]["partner_inference_id"])
        if added_inference_timestamps > 0:
            logger.info(
                f"{added_inference_timestamps} rows were missing inference_timestamp fields, so the current "
                f"time was populated"
            )
        if added_gt_timestamps > 0:
            logger.info(
                f"{added_gt_timestamps} rows were missing ground_truth_timestamp fields, so the current time "
                f"was populated"
            )
        if added_partner_inference_ids > 0:
            logger.info(
                f"{added_partner_inference_ids} rows were missing partner_inference_id fields, so UUIDs were "
                f"generated, see return values"
            )

        if self.input_type == InputType.Image:
            resp = self._upload_cv_inferences(inferences=inferences)
            self._attempt_close_batches(complete_batch, batch_counts)
            return resp.json()

        # send inferences to backend
        inference_ingestion_endpoint = f"/models/{self.id}/inferences"
        resp = self._client.post(
            inference_ingestion_endpoint,
            json=inferences,
            return_raw_response=True,
            validation_response_code=HTTPStatus.MULTI_STATUS,
        )
        (
            user_failures,
            internal_failures,
        ) = validation.validate_multistatus_response_and_get_failures(
            resp, raise_on_failures=(not fail_silently)
        )
        if fail_silently and (len(user_failures) > 0) or (len(internal_failures) > 0):
            message = "not all inferences succeeded!"
            message += (
                f" user failures: {user_failures}." if len(user_failures) > 0 else ""
            )
            message += (
                f" internal failures: {internal_failures}."
                if len(internal_failures) > 0
                else ""
            )
            logger.error(message)

        parsed_response = resp.json()
        if "results" not in parsed_response.keys():
            logger.warning(f"no inference-level results in response")
        elif len(parsed_response["results"]) != len(sent_partner_inference_ids):
            logger.warning(
                f"response results length {len(parsed_response['results'])} does not match "
                f"partner_inference_ids list length {len(sent_partner_inference_ids)}"
            )
        else:
            for i in range(len(parsed_response["results"])):
                parsed_response["results"][i]["partner_inference_id"] = (
                    sent_partner_inference_ids[i]
                )

        # complete batches
        self._attempt_close_batches(complete_batch, batch_counts)

        return parsed_response

    def _upload_cv_inferences(self, inferences: List[Dict[str, Any]]):
        cv_attr = self.get_image_attribute()
        image_zipper = ImageZipper()

        for inf in inferences:
            image_path = inf["inference_data"][cv_attr.name]
            image_zipper.add_file(image_path)

        zip_file = image_zipper.get_zip()
        headers = {"Content-Type": "multipart/form-data"}
        form_parts = {
            "image_data": ("images.zip", zip_file),
            "inference_data": ("inferences.json", json.dumps(inferences)),
        }

        endpoint = f"/models/{self.id}/inferences/file"
        # TODO: PE-983 - add validation
        return self._client.post(
            endpoint,
            json=None,
            files=form_parts,
            headers=headers,
            return_raw_response=True,
        )

    def _format_inference_request(
        self,
        inference_timestamp: Union[str, datetime],
        partner_inference_id: Optional[str] = None,
        model_pipeline_input=None,
        non_input_data=None,
        predicted_value=None,
        ground_truth=None,
    ):
        """Takes in an inference to send following the old sdk contract and converts the data to the request body
        of the new api format


        :param inference_timestamp: a mapping of the name of ground truth attributes to their value
        :param partner_inference_id: an external id (partner_inference_id) to assign to the inferences
        :param model_pipeline_input: a mapping of the name of pipeline input attributes to their value
        :param non_input_data: a mapping of the name of non-input data attributes to their value
        :param predicted_value: a mapping of the name of predicted value attributes to their value
        :param ground_truth: a mapping of the name of ground truth attributes to their value

        :return: dictionary object which can be used to send the inference
        """
        if model_pipeline_input is None:
            model_pipeline_input = {}
        if non_input_data is None:
            non_input_data = {}
        if predicted_value is None:
            predicted_value = {}

        model_pipeline_input.update(predicted_value)
        model_pipeline_input.update(non_input_data)
        inference = {
            "inference_timestamp": inference_timestamp,
            "partner_inference_id": partner_inference_id,
            "inference_data": model_pipeline_input,
        }

        if ground_truth is not None:
            inference["ground_truth_timestamp"] = inference_timestamp
            inference["ground_truth_data"] = ground_truth

        return inference

    @staticmethod
    def _replace_nans_and_infinities_in_dict(dict_to_update) -> Optional[Dict]:
        if dict_to_update is None:
            return None

        dict_to_return = {}

        for key, value in dict_to_update.items():
            if type(value) in (Series, list, np.ndarray):
                pass
            elif isna(value) or value in (np.Inf, -np.inf, np.inf):
                value = None
            dict_to_return[key] = value

        return dict_to_return

    @staticmethod
    def _convert_numpy_to_native(dict_to_update) -> Dict:
        final_dict = {}
        for k, v in dict_to_update.items():
            if isinstance(v, np.generic):
                final_dict[k] = v.item()
            else:
                final_dict[k] = v
        return final_dict

    @arthur_excepted("failed to send inference")
    def send_inference(
        self,
        inference_timestamp: Union[str, datetime],
        partner_inference_id: str = "",
        model_pipeline_input=None,
        non_input_data=None,
        predicted_value=None,
        ground_truth=None,
    ):
        """
        .. deprecated:: 3.20.0
            Please use :func:`ArthurModel.send_inferences()` to send a single inference.

        :param inference_timestamp: timestamp for inference to send; generated by external partner (not Arthur)
        :param partner_inference_id: an external id (partner_inference_id) to assign to the inferences
        :param model_pipeline_input: a mapping of the name of pipeline input attributes to their value
        :param non_input_data: a mapping of the name of non-input data attributes to their value
        :param predicted_value: a mapping of the name of predicted value attributes to their value
        :param ground_truth: a mapping of the name of ground truth attributes to their value

        :return: Upload status response in the following format:

         .. code-block:: JSON

            {
                "counts": {
                    "success": 0,
                    "failure": 0,
                    "total": 0
                },
                "results": [
                    {
                        "message": "success",
                        "status": 200
                    }
                ]
            }

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data write
        """
        logger.warning(
            "DEPRECATION WARNING: The ArthurModel.send_inference() method is deprecated. Please "
            "use ArthurModel.send_inferences() to send a single inference."
        )

        if predicted_value is None:
            predicted_value = {}
        if non_input_data is None:
            non_input_data = {}
        if model_pipeline_input is None:
            model_pipeline_input = {}

        self._check_model_save(msg="Must save model before sending inferences.")

        inference = self._format_inference_request(
            inference_timestamp=inference_timestamp,
            partner_inference_id=partner_inference_id,
            model_pipeline_input=ArthurModel._replace_nans_and_infinities_in_dict(
                model_pipeline_input
            ),
            non_input_data=ArthurModel._replace_nans_and_infinities_in_dict(
                non_input_data
            ),
            predicted_value=ArthurModel._replace_nans_and_infinities_in_dict(
                predicted_value
            ),
            ground_truth=ArthurModel._replace_nans_and_infinities_in_dict(ground_truth),
        )
        return self.send_inferences([inference])

    @arthur_excepted("failed to update inference ground truths")
    def update_inference_ground_truths(
        self,
        ground_truths: Union[
            List[Dict[str, Any]], Dict[str, List[Any]], DataFrame, Sequence[Any]
        ],
        partner_inference_ids: Optional[Sequence[str]] = None,
        ground_truth_timestamps: Optional[Sequence[Union[datetime, str]]] = None,
        tz: Optional[str] = None,
        fail_silently: bool = False,
    ):
        """Updates inferences with the supplied ground truth values

        For an introduction to sending data to Arthur,
        see https://docs.arthur.ai/user-guide/basic_concepts.html#sending-data-to-arthur

        The ``ground_truth`` parameter may contain all the required data, or only the data for the attributes from
        Stage.GroundTruth if metadata is supplied separately. At a minimum, Stage.GroundTruth attribute data and
        ``partner_inference_id`` should be passed in, either along with the attribute data in the ``ground_truths``
        parameter, or in the ``partner_inference_ids`` parameter.
        Additionally, a ``ground_truth_timestamp`` field is required by the Arthur API, but this will be generated if
        not supplied.

        .. seealso::
            To send large amounts of data or Parquet files, see :func:`ArthurModel.send_bulk_ground_truths()`

        **Examples:**

        A DataFrame containing all required values:

        .. code-block:: python

            y_test = [1, 0, 1]
            existing_inference_ids = [f"batch_1-inf_{i}" for i in len(y_test)]
            ground_truth_df = pd.DataFrame({"ground_truth_positive_labels": y_test,
                                            "ground_truth_negative_labels": 1 - y_test,
                                            "partner_inference_id": existing_inference_ids})
            arthur_model.update_inference_ground_truths(ground_truth_df)

        A single list of values, with partner_inference_ids supplied separately:

        .. code-block:: python

            y_test = [14.3, 19.6, 15.7]
            existing_inference_ids = [f"batch_1-inf_{i}" for i in len(y_test)]
            arthur_model.update_inference_ground_truths(y_test, partner_inference_ids=existing_inference_ids)

        All data in the inferences parameter in the format expected by the
        `Arthur API PATCH Inferences Endpoint
        <https://docs.arthur.ai/api-documentation/v3-api-docs.html#tag/inferences/paths/
        ~1models~1{model_id}~1inferences/patch>`_:

        .. code-block:: python

            ground_truth_data = [
                {
                    "partner_inference_id": "inf1",
                    "ground_truth_timestamp": "2021-06-16T16:53:45Z",
                    "ground_truth_data": {
                        "ground_truth_attr": 1
                    }
                }
            ]
            arthur_model.update_inference_ground_truths(ground_truth_data)

        A list of dicts without nested `ground_truth` fields:

        .. code-block:: python

            inference_data = [
                {
                    "partner_inference_id": "inf1",
                    "ground_truth_timestamp": "2021-06-16T16:53:45Z",
                    "ground_truth_attr": 1
                }
            ]
            arthur_model.send_inferences(inference_data)

        :param ground_truths: ground truth data to send, containing at least values for the ground truth attributes,
            and optionally ``ground_truth_timestamp`` and ``partner_inference_id``.
        :param partner_inference_ids: partner_inference_ids for the existing inferences to be updated, in a list-like
            format as strings. Required if not a field in ``ground_truths``.
        :param ground_truth_timestamps: the ground truth timestamps, in a list-like format as ISO-8601 strings or
            datetime objects. if no ground truth timestamps are supplied in ``inferences`` or this parameter,
            they will be generated from the current time. overwrites any timestamps in the ``ground_truths`` parameter.
        :param tz: datetime timezone object or timezone string
        :param fail_silently: if True, log failed inferences but do not raise an exception.
        :return: Upload status response in the following format:

            .. code-block:: json

                {
                    "counts": {
                        "success": 1,
                        "failure": 0,
                        "total": 1
                    },
                    "results": [
                        {
                            "message": "success",
                            "status": 200
                        }
                    ]
                }

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data write
        """
        self._check_model_save()

        # parse the input data into the expected format
        ground_truths = inferences_util.parse_stage_attributes(
            ground_truths, self.attributes, self.ground_truth_type
        )
        ground_truths = inferences_util.nest_inference_and_ground_truth_data(
            ground_truths, self.attributes
        )

        # if timestamps and/or partner inference ids are provided separately, add them
        if ground_truth_timestamps is not None:
            update_column_in_list_of_dicts(
                ground_truths, "ground_truth_timestamp", ground_truth_timestamps
            )
        if partner_inference_ids is not None:
            update_column_in_list_of_dicts(
                ground_truths, "partner_inference_id", partner_inference_ids
            )

        ground_truths = arthur_util.format_timestamps(ground_truths, tz)

        added_timestamps = 0
        current_iso_timestamp = datetime.now(pytz.utc).isoformat()
        for i in range(len(ground_truths)):
            ground_truths[i]["ground_truth_data"] = self._convert_numpy_to_native(
                ground_truths[i]["ground_truth_data"]
            )
            if "ground_truth_timestamp" not in ground_truths[i]:
                ground_truths[i]["ground_truth_timestamp"] = current_iso_timestamp
                added_timestamps += 1
        if added_timestamps > 0:
            logger.info(
                f"{added_timestamps} rows were missing ground_truth_timestamp fields, so the current time "
                f"was populated"
            )

        endpoint = f"/models/{self.id}/inferences"
        resp = self._client.patch(
            endpoint,
            json=ground_truths,
            return_raw_response=True,
            validation_response_code=HTTPStatus.MULTI_STATUS,
        )
        (
            user_failures,
            internal_failures,
        ) = validation.validate_multistatus_response_and_get_failures(
            resp, raise_on_failures=(not fail_silently)
        )
        if fail_silently and (len(user_failures) > 0) or (len(internal_failures) > 0):
            message = "not all ground truth updates succeeded!"
            message += (
                f" user failures: {user_failures}." if len(user_failures) > 0 else ""
            )
            message += (
                f" internal failures: {internal_failures}."
                if len(internal_failures) > 0
                else ""
            )
            logger.error(message)

        return resp.json()

    def _get_inference_count(self, with_ground_truth=True):
        query = {"select": [{"function": "count"}]}
        if with_ground_truth:
            # query from ground truth
            query["from"] = "ground_truth"
            # add a filter for ground truth not null for each ground truth attribute
            gt_attrs = self.get_attributes(stage=Stage.GroundTruth)
            query["filter"] = [
                {"property": a.name, "comparator": "NotNull"} for a in gt_attrs
            ]
        return self.query(query)

    def await_inferences(
        self, min_count: int = 1, with_ground_truth=True, timeout_min=5
    ) -> None:
        """Await a minimum number of inferences being available for querying

        :param min_count: Minimum number of inferences present for success (default 1)
        :param with_ground_truth: if True, only count inferences with corresponding ground truth values
        :param timeout_min: max number of minutes to wait before timing out
        :return: None
        :raises TimeoutError: if time limit is exceeded
        """
        logger.info(
            "Inferences usually become available for analysis in seconds, but it can take up to a few minutes. "
            "This function will report when the inferences are ready for your analysis."
        )
        poll_interval_sec = 5

        # fetch inference count and return if nonzero
        start_time = datetime.now()
        inf_count = self._get_inference_count(with_ground_truth=with_ground_truth)[0][
            "count"
        ]
        if inf_count >= min_count:
            logger.info("Inferences are now ready for analysis.")
            return
        # otherwise, begin repeating the above until timeout
        while (
            datetime.now() - start_time + timedelta(seconds=poll_interval_sec)
        ) <= timedelta(minutes=timeout_min):
            time.sleep(poll_interval_sec)
            inf_count = self._get_inference_count(with_ground_truth=with_ground_truth)[
                0
            ]["count"]
            if inf_count > min_count:
                logger.info("Inferences are now ready for analysis.")
                return

        raise TimeoutError(
            f"Wait time of {timeout_min} minutes exceeded while awaiting inferences"
        )

    @arthur_excepted("failed to binarize")
    def binarize(self, attribute_value):
        """Creates a binary class probability based on classes defined in a :py:attr:`.ModelType.Multiclass` model

        This function is only valid for models with two PredictedValue attributes
        which correspond to the positive and negative probabilities of a binary classifier

        .. code-block:: python

            # creates a binary class probability
            # evaluating the model's two predicted values against this value
            model.binarize({'ground_truth_column' : value})

        :param attribute_value: a mapping of the name of a predicted value attribute to its value

        :return: A two-value dictionary with probabilities for both predicted classes.
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """

        if len(attribute_value) > 1:
            raise UserValueError(
                "A dictionary containing a key, value pair for one ground truth attribute is required"
            )

        name, value = attribute_value.popitem()
        name = str(name)
        predicted_value = self.get_attributes(Stage.PredictedValue)
        if name not in [attr.name for attr in predicted_value]:
            raise UserValueError(
                f"Attribute {name} not found in {Stage.PredictedValue}"
            )

        valid_type = (
            lambda attr: attr.value_type == ValueType.Float
            and attr.min_range == 0.0
            and attr.max_range == 1.0
        )
        if len(predicted_value) == 2 and all(
            [valid_type(attr) for attr in predicted_value]
        ):
            return dict(
                [
                    (attr.name, value if attr.name == name else 1 - value)
                    for attr in predicted_value
                ]
            )
        else:
            raise MethodNotApplicableError(
                "This model is not a binary classification model."
            )

    @arthur_excepted("failed to one hot encode")
    def one_hot_encode(self, value):
        """Creates a one hot encoding of a class label based on classes defined in a :py:attr:`.ModelType.Multiclass`
        model

        This function does not modify your model's attributes.

        .. code-block:: python

            arthur_model.one_hot_encode('attribute_name')

        :param value: the name of the ground truth attribute to one-hot-encode

        :return: A dictionary with a one hot encoding of possible ground truth values.
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        name = str(value)
        ground_truth = self.get_attribute_names(stage=Stage.GroundTruth)
        if name not in ground_truth:
            raise UserValueError(f"Attribute {name} not found in {Stage.GroundTruth}")
        elif self.output_type != OutputType.Multiclass:
            raise MethodNotApplicableError("This model is not a Multiclass model")
        else:
            return dict(
                [
                    (attr_name, 1 if attr_name == name else 0)
                    for attr_name in ground_truth
                ]
            )

    def _send_files(
        self,
        endpoint: str,
        file_name: str,
        directory_path: Optional[str] = None,
        data: Optional[DataFrame] = None,
        files: Optional[
            List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]]
        ] = None,
        initial_form_data: Optional[Dict[str, Any]] = None,
        retries: int = 0,
    ):
        self._check_model_save(msg="Must save model before uploading reference data")

        if (
            directory_path is None
            and data is None
            and (files is None or len(files) == 0)
        ):
            raise MissingParameterError(
                "Either directory_path, data, or files must be provided"
            )

        if data is not None:
            if isinstance(data, DataFrame):
                is_ref_data = True if file_name == "reference_data" else False
                directory_path = self.convert_dataframe(
                    df=data, is_ref_data=is_ref_data
                )
            else:
                raise UnexpectedTypeError(
                    "Expected a pandas.DataFrame in the 'data' parameter"
                )

        if self.input_type == InputType.Image:
            logger.info("Processing image data, this may take a couple minutes")
            # to avoid large requets, we chunk image data into multiple zip files
            directory_path = (
                DatasetService.chunk_image_set_with_directory_path_or_files(
                    self.get_image_attribute().name, directory_path, files
                )
            )
            logger.info("Image processing complete!")

        if files is not None:
            _, file_info = DatasetService.send_files_iteratively(
                self,
                files,
                endpoint,
                file_name,
                additional_form_params=initial_form_data,
                retries=retries,
            )
        elif directory_path is not None:
            _, file_info = DatasetService.send_files_from_dir_iteratively(
                self,
                directory_path,
                endpoint,
                file_name,
                additional_form_params=initial_form_data,
                retries=retries,
            )

        # if image data or if data was passed as a DataFrame, all data has been chunked and moved to different
        # temporary directory than what the user passed in, ensure that is cleaned up
        if self.input_type == InputType.Image or data is not None:
            shutil.rmtree(directory_path)  # type: ignore

        return file_info

    def convert_dataframe(
        self,
        df: DataFrame,
        is_ref_data: bool,
        max_rows_per_file=DatasetService.MAX_ROWS_PER_FILE,
    ) -> str:
        """Convert a dataframe to file(s) named {model.id}-{chunk_num}.{extension} in the system tempdir

        The created files will be in the format in which the Arthur API expects to receive data. Users of this function
        are expected to clean up the created directory when they are done using it.
        `extension` is "parquet" if model types are parquet ingestible, "json" otherwise. `chunk_num` is 0 if the size
        of the dataframe is under the `max_rows_per_file` limit, otherwise it's an id referring to which chunk of
        the dataframe the file represents.

        :param df: the dataframe to convert
        :param is_ref_data: True if dataframe being converted contains reference data, False if it contains inference or
         ground truth data.
        :param max_rows_per_file: the maximum number of rows per created file
        :returns: the name of the directory containing the created parquet or json files
        """
        # some model types can't ingest parquet data
        to_parquet = (
            self.input_type in PARQUET_INGESTIBLE_INPUT_TYPES
            and self.output_type in PARQUET_INGESTIBLE_OUTPUT_TYPES
        )

        temp_dir = tempfile.mkdtemp()
        num_chunks = ceil(len(df) / max_rows_per_file)
        for chunk in range(num_chunks):
            fname = self.id if self.id is not None else ""
            fname += f"-{chunk}.parquet" if to_parquet else f"-{chunk}.json"
            filename = os.path.join(temp_dir, fname)
            start_idx = chunk * max_rows_per_file
            end_idx = (chunk + 1) * max_rows_per_file
            if to_parquet:
                df.iloc[start_idx:end_idx].to_parquet(
                    filename,
                    index=False,
                    allow_truncated_timestamps=True,
                    row_group_size=DatasetService.ROW_GROUP_SIZE,
                    engine="pyarrow",
                )
            else:  # write data to json files instead of parquet
                if is_ref_data:
                    data = self._ref_df_to_json(data=df.iloc[start_idx:end_idx])
                else:
                    data_list = self._format_inferences(
                        inferences=df.iloc[start_idx:end_idx], format_timestamps=True
                    )
                    data = json.dumps(data_list, indent=4)
                with open(filename, "w") as outfile:
                    outfile.write(data)
        return temp_dir

    def _transform_json_reference_data(
        self,
        directory_path: Optional[str] = None,
        files: Optional[
            List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]]
        ] = None,
    ) -> Tuple[List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]], str]:
        """Transforms reference data saved as .json files to the format expected by the backend

        Eg. [{"age": 12, "predicted_year": 1990, "ground_truth_attr": 2011}] will be transformed to
        [{"reference_data: {"age": 12, "predicted_year": 1990, "ground_truth_attr": 2011}}].
        If parquet files are also contained in the directory or files list passed, they will be unchanged and still
        included in the returned list of files.

        :param directory_path: path to directory with reference data
        :param files: list of files with reference data
        :return: (file_list, temp_dir) tuple where List is a list of files containing transformed reference data and
            temp_dir is the temporary directory created which will need to be cleaned up when the transformed files are
            no longer needed.
        :raises: UserValueError: Parameter is invalid or json data is not in a valid format
        """
        if directory_path is None and (files is None or len(files) == 0):
            raise UserValueError(
                "directory_path and files cannot both be None or empty lists"
            )

        temp_dir = tempfile.mkdtemp()
        all_files: List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]] = []
        json_files: List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]] = (
            []
        )
        if directory_path is not None:
            json_files = core_util.retrieve_json_files(directory_path)
            all_files = core_util.retrieve_parquet_files(directory_path)
        elif files is not None:
            for file in files:
                if _get_json_data(file) is not None:
                    json_files.append(file)
                else:
                    all_files.append(file)

        for i in range(len(json_files)):  # transform json files if needed
            file = json_files[i]
            reference_data = _get_json_data(file)

            # validate data types
            if not isinstance(reference_data, list):
                shutil.rmtree(temp_dir)
                raise UserValueError(
                    "json data is not in a valid format (list of dicts with reference data)"
                )
            for j in range(len(reference_data)):
                if not isinstance(reference_data[j], dict):
                    shutil.rmtree(temp_dir)
                    raise UserValueError(
                        "json data is not in a valid format (list of dicts with reference data)"
                    )

            transformed_reference_data = inferences_util.nest_reference_data(
                reference_data, self.attributes
            )

            # write transformed json file to temp directory
            with open(
                os.path.join(temp_dir, f"reference-data-transformed-{i}.json"), "w"
            ) as open_file:
                ref_data_json = json.dumps(transformed_reference_data, indent=4)
                open_file.write(ref_data_json)
            all_files.append(
                os.path.join(temp_dir, f"reference-data-transformed-{i}.json")
            )
        return all_files, temp_dir

    @arthur_excepted("failed to set reference data")
    def set_reference_data(
        self,
        directory_path: Optional[str] = None,
        data: Optional[Union[DataFrame, Series]] = None,
        files: Optional[
            List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]]
        ] = None,
    ):
        """Validates and sets the reference data for the given stage to the provided data.

        For an introduction to reference data, see https://docs.arthur.ai/docs/preparing-for-onboarding#reference-dataset

        To set reference data at the same time as inferring the model schema, see :func:`ArthurModel.build()`
        To infer the model schema without setting reference data, see :func:`ArthurModel.infer_schema()`

        .. code-block:: python

            # reference dataframe of model inputs
            reference_set = ...

            # produce model predictions on reference set
            # in this example, the predictions are classification probabilities
            preds = model.predict_proba(reference_set)

            # assign the column corresponding to the positive class
            # as the `pred` attribute in the reference data
            reference_set["pred"] = preds[:, 1]

            # set ground truth labels
            reference_set["gt"] = ...

            # configure the ArthurModel to use this dataframe as reference data
            arthur_model.set_reference_data(data=reference_set)

        Either directory_path or data must be provided. Additionally, there must be
        one column per `ModelPipelineInput` and `NonInput` attribute. If a directory_path is provided, all data in
        parquet or json files in the directory will be considered reference data to be set.

        For Image models, the image file path should be included as the image atribute value, in either
        the parquet files specified by `directory_path` or the DataFrame provided.

        To set reference data using json files, the files should contain a list of dicts where each element of the list
        is a new reference item and the keys in each dict are the attribute names.

        :param directory_path: file path to a directory of parquet and/or json files to upload for batch data
        :param data: a DataFrame or Series containing the ground truth data
        :param files: a list of open json/parquet files or a list of paths to openable json/parquet files containing
            reference data
        :return: Returns a tuple, the first variable is the response from sending the reference set and the second
            is the response from closing the dataset.
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: reference_data write
        """
        if (
            directory_path is None
            and data is None
            and (files is None or len(files) == 0)
        ):
            raise MissingParameterError(
                "Either directory_path, data, or files must be provided"
            )

        if not self.model_is_saved():
            if data is not None:
                self.reference_dataframe = data
                return
            else:
                raise UserTypeError(
                    "Can only set reference data for an unsaved model using a DataFrame. Please save "
                    "your model first to send Parquet files or set reference data with the 'data' "
                    "parameter."
                )

        temp_dir = ""
        if data is not None:
            data = core_util.standardize_pd_obj(
                data,
                dropna=False,
                replacedatetime=False,
                attributes=self.attributes_type_dict,
            )
            data = core_util.series_to_df(data)
        else:  # transform any json files into expected formatting
            files, temp_dir = self._transform_json_reference_data(directory_path, files)
            directory_path = None

        endpoint = f"/models/{self.id}/reference_data"
        num_rows = 0
        res = self._send_files(endpoint, "reference_data", directory_path, data, files)

        ref_set_close_res = None
        if res[DatasetService.COUNTS][DatasetService.FAILURE] != 0:
            logger.warning(
                f"{res[DatasetService.COUNTS][DatasetService.FAILURE]} inferences failed to upload"
            )
            logger.warning(
                "Reference dataset auto-close was aborted because not all "
                "inferences in the reference set were successfully uploaded"
            )
        else:
            if data is None:
                if directory_path is not None:
                    files = core_util.retrieve_json_files(
                        directory_path
                    ) + core_util.retrieve_parquet_files(directory_path)
                num_rows = self._count_json_num_rows(
                    files
                ) + self._count_parquet_num_rows(files)
            else:
                num_rows = len(data)

            if num_rows == 0:
                if temp_dir != "":
                    shutil.rmtree(temp_dir)
                raise UserValueError("data provided does not have any rows")

            ref_set_close_res = self._close_dataset(
                f"/models/{self.id}/reference_data", num_rows
            )
        if temp_dir != "":
            shutil.rmtree(temp_dir)
        return res, ref_set_close_res

    def _ref_df_to_json(self, data: DataFrame, format_timestamps: bool = True) -> str:
        """Standardizes and converts reference dataframe to json string

        :param data: reference dataset
        :param format_timestamps: True if timestamp columns still need to be reformatted as ISO-8601 strings from
         datetime objects (which is required before json serialization), False otherwise
        :return: standardized reference dataset as json string
        """
        # format df as nested list of dicts
        references = core_util.dataframe_like_to_list_of_dicts(data)
        references = inferences_util.nest_reference_data(references, self.attributes)

        # timestamps (any datetime objects) must be isoformatted strings to allow json serialization
        timestamp_attributes = (
            self.get_attribute_names(value_type=ValueType.Timestamp)
            if format_timestamps
            else None
        )
        time_series_attributes = self.get_attribute_names(
            value_type=ValueType.TimeSeries
        )
        references = arthur_util.format_timestamps(
            references,
            is_reference_data=True,
            timestamp_attributes=timestamp_attributes,
            time_series_attributes=time_series_attributes,
        )

        # do more numpy standardization
        for i in range(len(references)):
            references[i][InferenceType.REFERENCE_DATA] = (
                self._replace_nans_and_infinities_in_dict(
                    references[i][InferenceType.REFERENCE_DATA]
                )
            )
            references[i][InferenceType.REFERENCE_DATA] = self._convert_numpy_to_native(
                references[i][InferenceType.REFERENCE_DATA]
            )
        return json.dumps(references, indent=4)

    def _format_inferences(
        self,
        inferences: Union[List[Dict[str, Any]], Dict[str, List[Any]], DataFrame],
        format_timestamps: bool,
        predictions: Optional[
            Union[List[Dict[str, Any]], Dict[str, List[Any]], DataFrame, Sequence[Any]]
        ] = None,
        inference_timestamps: Optional[Sequence[Union[datetime, str]]] = None,
        ground_truths: Optional[
            Union[List[Dict[str, Any]], Dict[str, List[Any]], DataFrame, Sequence[Any]]
        ] = None,
        ground_truth_timestamps: Optional[Sequence[Union[datetime, str]]] = None,
        tz: Optional[str] = None,
        partner_inference_ids: Optional[Sequence[str]] = None,
    ) -> List[Dict[str, Any]]:
        """Format inference data to be sent to the Arthur API.

        The `inferences` parameter may contain all the inference data, or only the input data if predictions and
        metadata are supplied separately. At a minimum, input data and predictions should be passed in.

        Format of returned inferences:
                .. code-block:: python

            [
                inference_data = [
                    {
                        "inference_timestamp": "2021-06-16T16:52:11Z",
                        "partner_inference_id": "inf1",
                        "batch_id": "batch1",
                        "inference_data": {
                            "input_attr": 2,
                            "predicted_attr": 0.6
                        },
                        "ground_truth_timestamp": "2021-06-16T16:53:45Z",
                        "ground_truth_data": {
                            "ground_truth_attr": 1
                        }
                    }
                ],
            ]

        :param inferences: inference data to send; data must contain input values and may optionally contain predictions, ground
         truth, timestamps, partner inference ids, and batch IDs
        :param format_timestamps: True if timestamp columns still need to be reformatted as ISO-8601 strings from
         datetime objects (which is required before json serialization), False otherwise
        :param predictions: the model predictions, in a table-like format for one or more columns or a list-like format
         if the model has only one predicted column (NOTE: this overwrites any predictions supplied in the `inferences` parameter)
        :param inference_timestamps: the inference timestamps; a list-like format of ISO-8601 strings or datetime
         objects (NOTE: this overwrites any timestamps in the `inferences` parameter)
        :param ground_truths: the optional ground truth data; a table-like format for one or more columns or a list-like
         format if the model has only one ground truth column (NOTE: this overwrites any ground truth values
         supplied in the `inferences` parameter)
        :param ground_truth_timestamps: the ground truth timestamps; a list-like format of ISO-8601 strings or
         datetime objects (NOTE: this overwrites any timestamps in the `inferences`parameter)
        :param tz: datetime timezone object or timezone string
        :param partner_inference_ids: partner_inference_ids to be attached to these inferences, which can be used to
         send ground truth data later or retrieve specific inferences sent as a list-like format containing strings

        :return: standardized inference dataset as json string
        """
        # first map initial arg into list-of-dicts format, it may be flat (all fields in top-level dict) or nested
        #  (with model attributes nested under inference_data)
        inferences = core_util.dataframe_like_to_list_of_dicts(inferences)

        # if inference_data and/or gt_data are not nested, nest them
        # with 25 attributes this runs at about 150,000 rows / sec, not terribly slow but could definitely be better
        inferences = inferences_util.nest_inference_and_ground_truth_data(
            inferences, self.attributes
        )

        # if predictions and/or ground truth are provided separately, add them
        if predictions is not None:
            inferences_util.add_predictions_or_ground_truth(
                inferences, predictions, self.attributes, Stage.PredictedValue
            )
        if ground_truths is not None:
            inferences_util.add_predictions_or_ground_truth(
                inferences, ground_truths, self.attributes, self.ground_truth_type
            )
        # if timestamps and/or partner inference ids are provided separately, add them
        if inference_timestamps is not None:
            update_column_in_list_of_dicts(
                inferences,
                TimestampInferenceType.INFERENCE_TIMESTAMP,
                inference_timestamps,
            )
        if ground_truth_timestamps is not None:
            update_column_in_list_of_dicts(
                inferences,
                TimestampInferenceType.GROUND_TRUTH_TIMESTAMP,
                ground_truth_timestamps,
            )
        if partner_inference_ids is not None:
            update_column_in_list_of_dicts(
                inferences, "partner_inference_id", partner_inference_ids
            )

        # timestamps (any datetime objects) must be sent as isoformatted strings for backend compatibility
        timestamp_attributes = (
            self.get_attribute_names(value_type=ValueType.Timestamp)
            if format_timestamps
            else None
        )
        time_series_attributes = self.get_attribute_names(
            value_type=ValueType.TimeSeries
        )
        inferences = arthur_util.format_timestamps(
            inferences,
            tz=tz,
            timestamp_attributes=timestamp_attributes,
            time_series_attributes=time_series_attributes,
        )

        # do numpy standardization
        for i in range(len(inferences)):
            inferences[i][InferenceType.INFERENCE_DATA] = (
                self._replace_nans_and_infinities_in_dict(
                    inferences[i][InferenceType.INFERENCE_DATA]
                )
            )
            inferences[i][InferenceType.INFERENCE_DATA] = self._convert_numpy_to_native(
                inferences[i][InferenceType.INFERENCE_DATA]
            )
            if InferenceType.GROUND_TRUTH_DATA in inferences[i].keys():
                inferences[i][InferenceType.GROUND_TRUTH_DATA] = (
                    self._convert_numpy_to_native(
                        inferences[i][InferenceType.GROUND_TRUTH_DATA]
                    )
                )

        return inferences

    @arthur_excepted("failed to send bulk ground truths")
    def send_bulk_ground_truths(
        self,
        directory_path: Optional[str] = None,
        data: Optional[Union[DataFrame, Series]] = None,
        files: Optional[
            List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]]
        ] = None,
    ):
        """Uploads a large batch of ground truth values to Arthur

        Uploads a DataFrame or directory containing parquet files to the Arthur bulk inferences ingestion endpoint.
        Recommended for uploads of >100,000 rows of data.

        :param directory_path: file path to a directory of parquet and/or json files containing ground truth data. This
            should be used if and only if `data` is not provided. If a directory_path is provided,
            all data in parquet or json files in the directory will be considered ground truth data to be sent.
        :param data: a DataFrame or Series containing the ground truth data. Required if `directory_path` is not
            provided, and cannot be populated it `directory_path` is not provided.
        :param files: a list of open json/parquet files or a list of paths to openable json/parquet files
        :return: Upload status response in the following format:

            .. code-block:: JSON

                {
                    "counts": {
                        "success": 0,
                        "failure": 0,
                        "total": 0
                    },
                    "results": [
                        {
                            "message": "success",
                            "status": 200
                        }
                    ]
                }

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data write
        """
        self._check_model_save()

        endpoint = f"/models/{self.id}/inferences/file"
        num_rows = 0
        parquet_files: List[Path] = []
        json_files: List[Path] = []

        if (
            directory_path is None
            and data is None
            and (files is None or len(files) == 0)
        ):
            raise MissingParameterError(
                "Either directory_path, data, or files must be provided"
            )

        if data is not None:
            if isinstance(data, Series):
                data = data.to_frame()

            if isinstance(data, DataFrame):
                num_rows = len(data)
                data = core_util.standardize_pd_obj(
                    data,
                    dropna=False,
                    replacedatetime=False,
                    attributes=self.attributes_type_dict,
                )
            else:
                raise UserTypeError(
                    "Unsupported data type: a pandas.DataFrame is required"
                )
        elif directory_path is not None:
            parquet_files += core_util.retrieve_parquet_files(directory_path)
            num_rows = self._count_parquet_num_rows(parquet_files)
            json_files += core_util.retrieve_json_files(directory_path)
            num_rows += self._count_json_num_rows(json_files)

        if num_rows == 0 and files is None:
            raise UserValueError("data provided does not have any rows")

        prepped_data = (
            None
            if data is None
            else inferences_util.add_inference_metadata_to_dataframe(
                data, self.attributes
            )
        )

        # send parquet files or prepped data
        if prepped_data is not None or parquet_files or json_files or files:
            return self._send_files(
                endpoint,
                InferenceType.GROUND_TRUTH_DATA,
                directory_path,
                prepped_data,
                files,
                retries=INFERENCE_DATA_RETRIES,
            )

    @arthur_excepted("failed to send batch ground truths")
    def send_batch_ground_truths(
        self,
        directory_path: Optional[str] = None,
        data: Optional[Union[DataFrame, Series]] = None,
    ):
        """
        .. deprecated:: 3.10.0
            Please use :func:`ArthurModel.send_bulk_ground_truths()` for both streaming and batch data.

        :param directory_path: file path to a directory of parquet and/or json files containing ground truth data
        :param data:  a DataFrame or Series containing the reference data for the :py:class:`Stage`

        :return: Upload status response in the following format:

            .. code-block:: JSON

                {
                    "counts": {
                        "success": 1,
                        "failure": 0,
                        "total": 1
                    },
                    "results": [
                        {
                            "message": "success",
                            "status": 200
                        }
                    ]
                }
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        logger.warning(
            "DEPRECATION WARNING: The ArthurModel.send_batch_ground_truths() method is deprecated. Please "
            "use ArthurModel.send_bulk_ground_truths() for both streaming and batch data."
        )
        return self.send_bulk_ground_truths(directory_path=directory_path, data=data)

    @arthur_excepted("failed to send bulk inferences")
    def send_bulk_inferences(
        self,
        batch_id: Optional[str] = None,
        directory_path: Optional[str] = None,
        data: Optional[DataFrame] = None,
        files: Optional[
            List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]]
        ] = None,
        complete_batch: bool = True,
        ignore_join_errors: bool = FALSE_DEFAULT_IGNORE_JOIN_ERRORS,
        wait_for_enrichments: bool = False,
    ):
        # TODO [OBS-563]: we are setting wait_for_enrichments to False by default, but we plan on setting it to True
        #  after February 1, 2024
        """Uploads a large batch of inferences to Arthur

        Uploads a DataFrame or directory containing parquet and/or json files to the Arthur bulk inferences ingestion endpoint.
        Recommended for uploads of >100,000 rows of data.

        Validates and uploads parquet and/or json files containing columns for inference data, partner_inference_id,
        inference_timestamp, and optionally a batch_id. Either directory_path or data must be
        specified.

        .. seealso::
            To send ground truth for your inferences, see :func:`ArthurModel.send_bulk_ground_truth()`

        The columns for predicted attributes should follow the column format specified in
        ``add_<modeltype>_classifier_output_attributes()``.  Additionally, ``partner_inference_id``,
        must be specified for all inferences unless ``ignore_join_errors`` is True.

        :param batch_id: string id for the batch to upload; if supplied, this will override any batch_id column
            specified in the provided dataset
        :param directory_path: file path to a directory of parquet and/or json files containing inference data. This
            should be used if and only if `data` is not provided. If a directory_path is provided,
            all data in parquet or json files in the directory will be considered inferences to be sent.
        :param data: a DataFrame or Series containing the inference data. Required if ``directory_path`` is not
            provided, and cannot be populated if ``directory_path`` is not provided.
        :param files: a list of open json/parquet files or a list of paths to openable json/parquet files
        :param complete_batch: Defaults to true and will automatically close a batch once it is sent
        :param ignore_join_errors: if True, allow inference data without ``partner_inference_id`` or ground truth data
        :param wait_for_enrichments: if True, wait until all the model enrichments are in a ready state before sending
         inferences. Defaults to False.

        :return: A tuple of the batch upload response and the close batch response.
            The batch upload response is in the following format:

            .. code-block:: JSON

                {
                    "counts": {
                        "success": 1,
                        "failure": 0,
                        "total": 1
                    },
                    "results": [
                        {
                            "message": "success",
                            "status": 200
                        }
                    ]
                }

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data write
        """
        if not self.is_batch:
            complete_batch = False

        initial_form_data = {"batch_id": (None, batch_id)}
        endpoint = f"/models/{self.id}/inferences/file"
        num_rows = 0
        parquet_files: List[Path] = []
        json_files: List[Path] = []

        if (
            directory_path is None
            and data is None
            and (files is None or len(files) == 0)
        ):
            raise MissingParameterError(
                "Either directory_path, data, or files must be provided"
            )

        if wait_for_enrichments:
            await_enrichments_ready(self)

        if data is not None:
            if isinstance(data, Series):
                data = data.to_frame()

            if isinstance(data, DataFrame):
                num_rows = len(data)
                data = core_util.standardize_pd_obj(
                    data,
                    dropna=False,
                    replacedatetime=False,
                    attributes=self.attributes_type_dict,
                )
            else:
                raise UserTypeError(
                    "Unsupported data type: a pandas.DataFrame is required"
                )
        elif directory_path is not None:
            parquet_files += core_util.retrieve_parquet_files(directory_path)
            num_rows = self._count_parquet_num_rows(parquet_files)
            json_files += core_util.retrieve_json_files(directory_path)
            num_rows += self._count_json_num_rows(json_files)

        if num_rows == 0 and files is None:
            raise UserValueError("data provided does not have any rows")

        prepped_data = (
            None
            if data is None
            else inferences_util.add_inference_metadata_to_dataframe(
                data, self.attributes, ignore_join_errors=ignore_join_errors
            )
        )

        # send parquet/json files or prepped data
        if prepped_data is not None or parquet_files or json_files or files:
            res = self._send_files(
                endpoint,
                InferenceType.INFERENCE_DATA,
                directory_path,
                prepped_data,
                files,
                initial_form_data=initial_form_data,
                retries=INFERENCE_DATA_RETRIES,
            )

        batch_res = None
        if res[DatasetService.COUNTS][DatasetService.FAILURE] != 0:
            logger.warning(
                f"{res[DatasetService.COUNTS][DatasetService.FAILURE]} inferences failed to upload"
            )
            if complete_batch:
                logger.warning(
                    "Batch auto-close was aborted because not all inferences were successfully uploaded"
                )
        elif complete_batch:
            batch_res = self.close_batch(
                batch_id, res[DatasetService.COUNTS][DatasetService.SUCCESS]
            )

        return res, batch_res

    def send_batch_inferences(
        self,
        batch_id: Optional[str],
        directory_path: Optional[str] = None,
        data: Optional[DataFrame] = None,
        complete_batch: bool = True,
    ):
        """Send many inferences at once

        .. deprecated:: 3.10.0
            Use :func:`ArthurModel.send_inferences()` to send batch or streaming data synchronously (recommended fewer
            than 100,000 rows), or :func:`ArthurModel.send_bulk_inferences()` to send many inferences or parquet and/or json files.

        :param batch_id: string id for the batch to upload; if supplied, this will override any batch_id column
            specified in the provided dataset
        :param data: a DataFrame containing the reference data.
        :param directory_path: file path to a directory of parquet and/or json files containing ground truth data
        :param complete_batch: Defaults to true and will automatically close a batch once it is sent
        :return: A tuple of the batch upload response and the close batch response.
            The batch upload response is in the following format:

            .. code-block:: JSON

                {
                    "counts": {
                        "success": 0,
                        "failure": 0,
                        "total": 0
                    },
                    "failures": []
                }

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        logger.warning(
            "DEPRECATION WARNING: The ArthurModel.send_batch_inferences() method is deprecated. Please use "
            "ArthurModel.send_inferences() or ArthurModel.send_bulk_inferences(). Both methods support "
            "batch and streaming models, simply supply a `batch_id` field for batch models or omit it for "
            "streaming models. Use send_bulk_inferences() to send a larger number of inferences "
            "(recommended for more than 100,000 rows) asynchronously, or to upload Parquet files directly."
        )
        return self.send_bulk_inferences(
            batch_id=batch_id,
            directory_path=directory_path,
            data=data,
            complete_batch=complete_batch,
        )

    def _count_parquet_num_rows(
        self,
        file_paths: Union[
            Optional[List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]]],
            List[Path],
        ],
    ) -> int:
        """Counts number of rows in parquet files

        If a file in file_paths is not a parquet file, it is ignored silently.

        :param file_paths: List of files with rows to be counted
        :return: Total number of rows
        """
        num_rows = 0
        if file_paths is None:
            return num_rows

        for file in file_paths:
            pqfile = _get_parquet_file(file)
            if pqfile is None:
                continue
            num_rows += pqfile.metadata.num_rows

        return num_rows

    def _count_json_num_rows(
        self,
        file_paths: Union[
            Optional[List[Union[str, Path, PathLike, BufferedReader, BufferedRandom]]],
            List[Path],
        ],
    ) -> int:
        """Counts number of rows in json files

        If a file in file_paths is not a json file, it is ignored silently.

        :param file_paths: List of files with rows to be counted
        :return: Total number of rows
        """
        num_rows = 0
        if file_paths is None:
            return num_rows
        for file_path in file_paths:
            json_data = _get_json_data(file_path)
            if json_data is None:
                continue
            # if the json data provided is a list, use the number of items as the number of rows; if it has a
            # different format, raise an error
            if type(json_data) == list:
                num_rows += len(json_data)
            else:
                raise UserValueError(
                    "json data is not in a valid format (list of inferences)"
                )

        return num_rows

    def _close_dataset(
        self, endpoint: str, num_inferences: Optional[int] = None
    ) -> Dict:
        body: Dict[str, Union[str, int]] = {"status": "uploaded"}
        if num_inferences is not None:
            body["total_record_count"] = num_inferences

        batch_res = self._client.patch(
            endpoint=endpoint,
            json=body,
            return_raw_response=True,
            retries=INFERENCE_DATA_RETRIES,
            validation_response_code=HTTPStatus.OK,
        )
        return {"dataset_close_result": batch_res.json()}

    @arthur_excepted("failed to close batch")
    def close_batch(self, batch_id: str, num_inferences: Optional[int] = None) -> Dict:
        """Closes the specified batch, optionally can supply the number of inferences that are contained in the batch

        :param batch_id: String batch_id associated with the batch that will be closed
        :param num_inferences: Optional number of inferences that are contained in the batch
        :return: Response of the batch close rest call
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data write
        """
        endpoint = f"/models/{self.id}/batches/{batch_id}"
        return self._close_dataset(endpoint, num_inferences)

    @arthur_excepted("failed to delete explainer")
    def delete_explainer(self) -> None:
        """Spin down the model explainability server

        After calling this function, explainability will have to be re-enabled
        if you want to compute feature importance scores for your model.

        :return: the server response

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: enrichment_config write
        """
        if not hasattr(self, "_explainer"):
            raise MethodNotApplicableError(
                f"There is no explainability server to delete for model {self.id}"
            )

        endpoint = f"/models/{self.id}/explainability"
        self._client.delete(
            endpoint,
            return_raw_response=True,
            validation_response_code=HTTPStatus.NO_CONTENT,
        )
        logger.info(f"Successfully removed explainability server for model {self.id}")

    @arthur_excepted("failed to archive model")
    def archive(self):
        """Archives the model with a DELETE request

        :return: the server response
        :raises Exception: the model has no ID, or the model has not been archived
        :permissions: model delete
        """
        self._check_model_save(msg="Cannot archive an unregistered model.")

        endpoint = f"/models/{self.id}"
        # TODO [TMJ]: REMOVE RETRIES...this is a temporary band-aid to deal with issues
        #             our archive endpoint has.
        self._client.delete(
            endpoint,
            return_raw_response=True,
            validation_response_code=HTTPStatus.NO_CONTENT,
            retries=3,
        )

    @arthur_excepted("failed to execute query")
    def query(self, body: Dict[str, Any], query_type="base"):
        """Execute query against the model's inferences.
        For full description of possible functions, aggregations, and transformations, see
        https://docs.arthur.ai/user-guide/api-query-guide/index.html

        :param body: dict
        :param query_type: str Can be either 'base', 'drift', or 'drift_psi_bucket_table'

        .. code-block:: python

            body = {
                       "select":[
                          {"property":"batch_id"},
                          {
                             "function":"count",
                             "alias":"inference_count"
                          }
                       ],
                       "group_by":[
                          {"property":"batch_id"}
                       ]
                    }

        .. code-block:: python

            body = {
                       "select":[,
                          {"property":"batch_id"},
                          {
                             "function":"rate",
                             "alias":"positive_rate",
                             "parameters":{
                                "property":"predicted_1",
                                "comparator":"gt",
                                "value":0.75
                             }
                          }
                       ],
                       "group_by":[
                          {"property":"batch_id"}
                       ]
                    }


        :return: the query response
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: query execute
        """
        self._check_model_save(msg="You must save model before querying.")

        endpoint = f"/models/{self.id}/inferences/query"
        if query_type == "base":
            pass
        elif query_type == "drift":
            endpoint = f"{endpoint}/data_drift"
        elif query_type == "drift_psi_bucket_table":
            endpoint = f"{endpoint}/data_drift_psi_bucket_calculation_table"
        else:
            raise UserValueError(
                f"Invalid query type '{query_type}', must be on of 'base', 'drift', or "
                f"'drift_psi_bucket_table'"
            )
        resp = self._client.post(
            endpoint,
            json=body,
            return_raw_response=True,
            validation_response_code=HTTPStatus.OK,
        )

        return resp.json()["query_result"]

    @arthur_excepted("failed to create metric")
    def create_metric(
        self,
        name: str,
        query: Dict[str, Any],
        is_data_drift: bool = False,
        metric_type: Optional[MetricType] = None,
        parameters: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """
        Creates a metric registered to this model and returns the UUID assigned to the newly created metric.

        This metric can be used to create alert rules on.

        For an introduction to creating metrics for alert rules,
        see https://docs.arthur.ai/user-guide/walkthroughs/metrics_alerts.html#creating-custom-metrics

        :param name: Name of the metric to create.
        :param query: Query which makes up the metric
        :param is_data_drift: Boolean to signal whether this query is a data drift metric or not.
        :param metric_type: Type associated with the metric to create. If this field is not supplied the metric type will
            automatically be filled in (enum: [model_output_metric, model_performance_metric, model_data_drift_metric,
            model_data_bound_metric])
        :param parameters: Optional list of parameters associated with the metric to create
        :return: UUID of the newly created metric
        :permissions: metric_query write
        """
        endpoint = f"/models/{self.id}/metrics"
        metric_endpoint = (
            f"{API_PREFIX}/models/{self.id}/inferences/query"
            if not is_data_drift
            else f"{API_PREFIX}/models/{self.id}/inferences/query/data_drift"
        )
        request_body = {
            "name": name,
            "query": query,
            "endpoint": metric_endpoint,
            "parameters": [] if parameters is None else parameters,
        }

        if metric_type:
            if metric_type not in MetricType.list():
                raise ArthurUserError(
                    f"Must use a metric_type from arthurai.core.alerts.MetricType: {MetricType.list()}"
                )
            request_body["type"] = metric_type

        resp = self._client.post(
            endpoint,
            json=request_body,
            return_raw_response=True,
            path_prefix=API_PREFIX_V4,
        )
        validation.validate_response_status(
            resp, expected_status_code=HTTPStatus.CREATED
        )
        return resp.json()["id"]

    @arthur_excepted("failed to retrieve metrics")
    def get_metrics(
        self,
        default_metrics: bool = False,
        metric_type: Optional[MetricType] = None,
        metric_id: Optional[str] = None,
        metric_name: Optional[str] = None,
        attribute_name: Optional[str] = None,
    ) -> List[Metric]:
        """Retrieves metrics associated with the current model. Can add optional filters to search with function parameters.
        :param default_metrics: If set to True will return only metrics that are automatically created by default for your model
        :param metric_type: MetricType to filter metric query with
        :param metric_id: Metric UUID to use in filtering metric search
        :param metric_name: Metric name filter to use in metric search
        :param attribute_name: Attribute name filter to use in metric search
        :return: list of metrics returned from metric search
        :permissions: metric_query read
        """
        if metric_id is not None:
            endpoint = f"/models/{self.id}/metrics/{metric_id}"
            resp = self._client.get(
                endpoint, return_raw_response=True, path_prefix=API_PREFIX_V4
            )
            validation.validate_response_status(
                resp, expected_status_code=HTTPStatus.OK
            )
            return [Metric.from_dict(resp.json())]
        else:
            query_params = {"expand": "type"}
            if default_metrics:
                query_params["default"] = "true"
            if metric_type:
                if metric_type not in MetricType.list():
                    raise ArthurUserError(
                        f"Must use a metric_type from arthurai.core.alerts.MetricType: {MetricType.list()}"
                    )
                query_params["type"] = metric_type
            if metric_name:
                query_params["metric_name"] = metric_name
            if attribute_name:
                query_params["attribute_name"] = attribute_name

            endpoint = f"/models/{self.id}/metrics"
            current_page = total_pages = 1
            metrics = []
            while current_page <= total_pages:
                query_params["page"] = str(current_page)
                resp = self._client.get(
                    endpoint,
                    params=query_params,
                    return_raw_response=True,
                    path_prefix=API_PREFIX_V4,
                )
                validation.validate_response_status(
                    resp, expected_status_code=HTTPStatus.OK
                )
                response_object = resp.json()
                json_metrics = response_object["metrics"]
                if len(json_metrics) == 0:
                    break
                metrics.extend([Metric.from_dict(m) for m in json_metrics])
                total_pages = response_object["total_pages"]
                current_page = response_object["page"] + 1

        return metrics

    @arthur_excepted("failed to create alert rule")
    def create_alert_rule(
        self,
        metric_id: str,
        bound: AlertRuleBound,
        threshold: NumberType,
        severity: AlertRuleSeverity,
        name: Optional[str] = None,
        lookback_period: Optional[NumberType] = None,
        subsequent_alert_wait_time: Optional[NumberType] = None,
        metric_parameters: Optional[Dict[str, Any]] = None,
        filters: Optional[Dict[str, Any]] = None,
    ) -> AlertRule:
        """Creates alert rules for the current model.

        For an introduction to alerts, see https://docs.arthur.ai/user-guide/basic_concepts.html#alerts

        For a guide to configuring alerts, see https://docs.arthur.ai/user-guide/walkthroughs/metrics_alerts.html#id1

        :param metric_id: unique id (UUID) of the metric to use to create an alert rule.
        :param name: A name for the alert rule, a default will be generated if this is not supplied.
        :param bound: Whether the alert is triggered crossing the threshold from above or below. Either AlertRuleBound.Upper or AlertRuleBound.Lower
        :param threshold: Threshold value of the alert rule. When the metric crosses this threshold, the alert is triggered.
        :param severity: AlertRuleSeverity of the alert which gets triggered when the metric violates the threshold of
                         the alert rule.
        :param lookback_period: The lookback time or "window length" in minutes to use when calculating the alert rule
                                metric. For example, a lookback period of 5 minutes for an alert rule on average
                                prediction will calculate average prediction for the past 5 minutes in a rolling window
                                format. This will default to 5 minutes
        :param subsequent_alert_wait_time: If metric continues to pass threshold this is the time in minutes to wait
                                           before triggering another alert. This defaults to 1 day. This does not need
                                           to be set for batch alerts.
        :param metric_parameters: mapping from metric parameter name to desired value
        :param filters: filters to use when evaluating the metric used in the alert rule
        :return: the created alert rule
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: alert_rule write
        """
        params = validate_parameters_for_alert(metric_parameters)
        alert_rule = AlertRule(
            name=name,
            bound=bound,
            threshold=threshold,
            metric_id=metric_id,
            severity=severity,
            lookback_period=lookback_period,
            subsequent_alert_wait_time=subsequent_alert_wait_time,
            metric_parameters=params,
            filters=filters,
        )

        endpoint = f"/models/{self.id}/alert_rules"
        resp = self._client.post(
            endpoint,
            json=alert_rule.to_dict(),
            return_raw_response=True,
            validation_response_code=HTTPStatus.OK,
        )

        return AlertRule.from_dict(resp.json())

    @arthur_excepted("failed to get model alert rules")
    def get_alert_rules(self, page: int = 1, page_size: int = 20) -> List[AlertRule]:
        """Returns a paginated list of alert rules registered to this model

        For an introduction to alerts, see https://docs.arthur.ai/user-guide/basic_concepts.html#alerts

        For a guide to configuring alerts, see https://docs.arthur.ai/user-guide/walkthroughs/metrics_alerts.html#id1

        :param page: page of alert rules to retrieve, defaults to 1
        :param page_size: number of alert rules to return per page, defaults to 20
        :return: List of :class:`arthurai.client.apiv3.AlertRule` objects
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: alert_rule read
        """
        endpoint = f"/models/{self.id}/alert_rules?page_size={page_size}&page={page}"
        resp = self._client.get(
            endpoint, return_raw_response=True, validation_response_code=HTTPStatus.OK
        )

        if "data" not in resp.json():
            raise ExpectedParameterNotFoundError(
                "An error occurred when retrieving alert rules: {0}".format(resp.json())
            )

        # This solves a problem noted by a bug in OBS-643: https://arthurai.atlassian.net/browse/OBS-643
        alert_rule_json_list = resp.json()["data"]
        if alert_rule_json_list is None:
            alert_rule_json_list = []

        alert_rules = []
        for rule in alert_rule_json_list:
            alert_rules.append(AlertRule.from_dict(rule))
        return alert_rules

    @arthur_excepted("failed to update alert rule")
    def update_alert_rule(
        self, alert_rule: AlertRule, alert_rule_id: Optional[str] = None
    ):
        """Updates alert rule fields included in the `alert_rule` object for the specified alert rule id. If the
        alert rules id field is present in the `alert_rule` parameter that is used otherwise `alert_rule_id`
        must be supplied

        For an introduction to alerts, see https://docs.arthur.ai/user-guide/basic_concepts.html#alerts

        For a guide to configuring alerts, see https://docs.arthur.ai/user-guide/walkthroughs/metrics_alerts.html#id1

        :param alert_rule: Object which contains fields to update on the specified alert rule
        :param alert_rule_id: If the alert rule id is not specified in the `alert_rule_to_update` object then this
                              must be provided to determine which alert rule to update.
        :return: Updates alert rule object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: alert_rule write
        """
        if alert_rule.id is None and alert_rule_id is None:
            raise MethodNotApplicableError(
                "alert_rule_to_update must have a valid id, if the alert rule has not been "
                "created yet call model.create_alert_rule(...)"
            )
        if alert_rule.metric_parameters is not None:
            alert_rule.metric_parameters = validate_parameters_for_alert(
                alert_rule.metric_parameters
            )

        alert_rule_id = alert_rule.id if alert_rule.id is not None else alert_rule_id
        alert_rule.id = None

        endpoint = f"/models/{self.id}/alert_rules/{alert_rule_id}"
        resp = self._client.patch(
            endpoint,
            json=alert_rule.to_dict(),
            return_raw_response=True,
            validation_response_code=HTTPStatus.OK,
        )

        return AlertRule.from_dict(resp.json())

    @arthur_excepted("failed to get model alerts")
    def get_alerts(
        self,
        page: int = 1,
        page_size: int = 500,
        status: Optional[str] = None,
        alert_rule_id: Optional[str] = None,
        batch_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
    ) -> List[Alert]:
        """Returns a paginated list of alert registered to this model.

        For an introduction to alerts, see https://docs.arthur.ai/user-guide/basic_concepts.html#alerts

        For a guide to configuring alerts, see https://docs.arthur.ai/user-guide/walkthroughs/metrics_alerts.html#id1

        :param page: page of alert rules to retrieve, defaults to 1
        :param page_size: number of alert rules to return per page, defaults to 500
        :param status: status of alert rule
        :param alert_rule_id: id of alert rule
        :param batch_id: constrain returned alert rules to this batch id
        :param start_time: constrain returned alert rules to after this time
        :param end_time: constrain returned alert rules to before this time
        :return: List of :class:`arthurai.client.apiv3.Alert` objects
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: alert read
        """
        endpoint = "/alerts"
        # construct query parameters dictionary to be passed into client.get()
        query_params = {
            "model_id": self.id,
            "page_size": page_size,
            "page": page,
            "status": status,
            "alert_rule_id": alert_rule_id,
            "batch_id": batch_id,
            "start_time": start_time,
            "end_time": end_time,
        }

        # remove empty parameters
        for k in query_params.copy().keys():
            if query_params[k] is None:
                query_params.pop(k)

        resp = self._client.get(
            endpoint,
            params=query_params,
            return_raw_response=True,
            validation_response_code=HTTPStatus.OK,
        )

        if "data" not in resp.json():
            raise ExpectedParameterNotFoundError(
                "An error occurred when retrieving alerts: {0}".format(resp.json())
            )

        alerts = []
        for rule in resp.json()["data"]:
            alerts.append(Alert.from_dict(rule))
        return alerts

    @arthur_excepted("failed to update alert")
    def update_alert(self, status: AlertStatus, alert_id: str) -> Alert:
        """Updates alert to have a particular status.

        For an introduction to alerts, see https://docs.arthur.ai/user-guide/basic_concepts.html#alerts

        For a guide to configuring alerts, see https://docs.arthur.ai/user-guide/walkthroughs/metrics_alerts.html#id1

        :param status: one of "resolved" or "acknowledged"
        :param alert_id: alert id
        :return: updated alert object
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: alert write
        """
        if status not in AlertStatus.list():
            raise ValueError(
                f"status={status} is not valid and must be one of {AlertStatus.list()}"
            )

        endpoint = f"/alerts/{alert_id}"
        resp = self._client.patch(
            endpoint,
            json={"status": status},
            return_raw_response=True,
            validation_response_code=HTTPStatus.OK,
        )

        return Alert.from_dict(resp.json())

    @arthur_excepted("failed to explain inference")
    def explain_inference(
        self,
        partner_inference_id: str,
        algorithm: str = "lime",
        page: int = 1,
        page_size: int = 500,
        n_samples: Optional[int] = None,
        sort: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Returns feature importance scores for each attribute of stage ModelPipelineInput

        :param partner_inference_id: the ID attached to the inference
        :param algorithm: the explanation algorithm ('lime' or 'shap') used to generate the feature importance scores
        :param page: the number of batches to split the results into
        :param page_size: the maximum number of inferences in each batch if returning inferences in batches
        :param n_samples: # local perturbations for explanation (if None, uses default from lime or shap)
        :param sort: option for the ordering of returned explanations
        :return: Upload status response in the following format:

            .. code-block:: JSON

                {
                    "explanation": [
                        {
                            "algorithm": "shap",
                            "predicted_attribute_name": "class_a",
                            "importance_scores": [
                                {
                                    "attribute_name": "feature_a",
                                    "explanation_value": 0.12,
                                    "tokens": [
                                        {
                                            "token": "dog",
                                            "position": 0,
                                            "explanation_value": 0.48
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "expected_value": [
                        {
                            "predicted_attribute_name": "feature_a",
                            "expected_value": 0.12
                        }
                    ]
                }
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data read
        """
        query_params: Dict[str, Any] = {}
        if algorithm.lower() not in ["lime", "shap"]:
            raise UserValueError("algorithm must be either lime or shap")
        query_params["algorithm"] = algorithm.lower()
        query_params["page"] = page
        query_params["page_size"] = page_size
        if n_samples is not None:
            query_params["n_samples"] = n_samples
        if sort is not None:
            # check if the sort type is in the listed options
            check_options = sort[1:] if sort[0] in ["+", "-"] else sort
            if check_options.lower() not in [
                "value",
                "word",
                "location",
                "attribute_name",
            ]:
                raise UserValueError(
                    "sort option muse be in ['value', 'word', 'location', 'attribute_name']"
                )
            query_params["sort"] = sort.lower()
        endpoint = f"/models/{self.id}/inferences/{partner_inference_id}/explanation"
        resp = self._client.get(endpoint, params=query_params, return_raw_response=True)
        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)
        return resp.json()

    @arthur_excepted("failed to get enrichments")
    def get_enrichments(self) -> Dict[str, Any]:
        """Returns configuration for all enrichments.

        For an introduction to enrichments, see https://docs.arthur.ai/user-guide/basic_concepts.html#enrichments

        For a guide to configuring enrichments, see https://docs.arthur.ai/user-guide/walkthroughs/enrichments.html

        :return: Upload status response in the following format:

            .. code-block:: JSON

                {
                    "anomaly_detection": {
                        "enabled": false
                    },
                    "explainability": {
                        "config": {
                            "python_version": "3.7",
                            "sdk_version": "3.0.11",
                            "streaming_explainability_enabled": false,
                            "user_predict_function_import_path": "entrypoint",
                            "shap_expected_values": "[0.7674405187893311, 0.23255948121066888]",
                            "model_server_cpu": "2",
                            "model_server_memory": "1Gi",
                            "model_server_max_replicas": "5",
                            "explanation_nsamples": 1000,
                            "explanation_algo": "lime",
                            "inference_consumer_cpu": "100m",
                            "inference_consumer_memory": "512Mi",
                            "inference_consumer_score_percent": "1.0",
                            "inference_consumer_thread_pool_size": "1",
                            "service_account_id": "8231affb-c107-478e-a1b4-e24e7f1f6619"
                        },
                        "enabled": true
                    }
                }
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: enrichment_config read
        """
        endpoint = f"/models/{self.id}/enrichments"
        resp = self._client.get(
            endpoint, return_raw_response=True, validation_response_code=HTTPStatus.OK
        )
        return resp.json()

    @arthur_excepted("failed to get enrichment")
    def get_enrichment(self, enrichment: Enrichment) -> Dict[str, Any]:
        """Returns configuration for the specified enrichment.

        For an introduction to enrichments, see https://docs.arthur.ai/user-guide/basic_concepts.html#enrichments

        For a guide to configuring enrichments, see https://docs.arthur.ai/user-guide/walkthroughs/enrichments.html

        :param enrichment: Enrichment constant
        :return: Enrichment config

            .. code-block:: JSON

                {
                    "enabled": true,
                    "config": {
                        "python_version": "3.7",
                        "sdk_version": "3.0.11",
                        "streaming_explainability_enabled": false,
                        "user_predict_function_import_path": "entrypoint",
                        "shap_expected_values": "[0.7674405187893311, 0.23255948121066888]",
                        "model_server_cpu": "2",
                        "model_server_memory": "1Gi",
                        "model_server_max_replicas": "5",
                        "explanation_nsamples": 1000,
                        "explanation_algo": "lime",
                        "inference_consumer_cpu": "100m",
                        "inference_consumer_memory": "512Mi",
                        "inference_consumer_score_percent": "1.0",
                        "inference_consumer_thread_pool_size": "1",
                        "service_account_id": "8231affb-c107-478e-a1b4-e24e7f1f6619"
                    }
                }
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: enrichment_config read
        """
        endpoint = f"/models/{self.id}/enrichments/{enrichment}"
        resp = self._client.get(
            endpoint, return_raw_response=True, validation_response_code=HTTPStatus.OK
        )
        return resp.json()

    @arthur_excepted("failed to update enrichments")
    def update_enrichments(
        self, enrichment_configs: Dict[Union[str, Enrichment], Any]
    ) -> Dict[str, Any]:
        """Update the configuration for 1 or more enrichments.

        For an introduction to enrichments, see https://docs.arthur.ai/user-guide/basic_concepts.html#enrichments

        For a guide to configuring enrichments, see https://docs.arthur.ai/user-guide/walkthroughs/enrichments.html

        :param enrichment_configs: Dict containing the configuration for each enrichment

            .. code-block:: json

                {
                    "anomaly_detection": {
                        "enabled": false
                    },
                    "explainability": {
                        "config": {
                            "streaming_explainability_enabled": false,
                            "explanation_nsamples": 1000,
                            "explanation_algo": "lime",
                            "inference_consumer_score_percent": "1.0"
                        },
                        "enabled": true
                    }
                    "hotspots": {
                        "enabled": false
                    }
                }
        :return: the resulting enrichments configuration
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: enrichment_config write
        """

        files = []
        # handle specifics for different enrichments
        if (
            Enrichment.Explainability in enrichment_configs
            and enrichment_configs[Enrichment.Explainability]["enabled"]
        ):
            explanationPackager = ExplanationPackager(
                self, **enrichment_configs[Enrichment.Explainability]["config"]
            )

            # check to see if user is trying to update files
            onePresent, allPresent = explanationPackager.contains_file_fields()
            if onePresent and not allPresent:
                raise MissingParameterError(
                    f"If updating model files for explainability, all of the following fields must be present in the config {ExplanationPackager.FILE_FIELDS}"
                )
            # package explainer files
            elif allPresent:
                explanationPackager.make_zip()
                explanationPackager.create()
                files += explanationPackager.get_request_files()
            # replace passed in config (has file specific fields) with actual config
            enrichment_configs[Enrichment.Explainability][
                "config"
            ] = explanationPackager.get_request_config()

        # build and make request
        headers = {"Content-Type": "multipart/form-data"}
        endpoint = f"/models/{self.id}/enrichments"
        data = {"config": json.dumps(enrichment_configs)}

        resp = self._client.patch(
            endpoint,
            json=data,
            files=files,
            headers=headers,
            return_raw_response=True,
            validation_response_code=HTTPStatus.ACCEPTED,
        )
        return resp.json()

    @arthur_excepted("failed to update enrichment")
    def update_enrichment(
        self,
        enrichment: Enrichment,
        enabled: Optional[bool] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Update the configuration for a single enrichment

        For an introduction to enrichments, see https://docs.arthur.ai/user-guide/basic_concepts.html#enrichments

        For a guide to configuring enrichments, see https://docs.arthur.ai/user-guide/walkthroughs/enrichments.html

        :param enrichment: the enrichment to update
        :param enabled: whether the enrichment should be enabled or disabled
        :param config: the configuration for the enrichment, None by default
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: enrichment_config write
        """

        data: Dict[str, Any] = {}
        if enabled is not None:
            data["enabled"] = enabled
        if config is not None:
            data["config"] = config
        return self.update_enrichments({enrichment: data})

    @arthur_excepted("failed to enable hotspots")
    def enable_hotspots(self):
        """Updates the hotspots Enrichment to be enabled

        .. seealso::
            This convenience function wraps :func:`ArthurModel.update_enrichment()`

        :permissions: enrichment_config write
        """
        self._check_model_save()

        if not self.input_type == InputType.Tabular:
            raise MethodNotApplicableError(
                "Hotspots may only be enabled on tabular models."
            )

        return self.update_enrichment(Enrichment.Hotspots, True)

    @arthur_excepted("failed to find hotspots")
    def find_hotspots(
        self,
        metric: AccuracyMetric = AccuracyMetric.Accuracy,
        threshold: float = 0.5,
        batch_id: Optional[str] = None,
        date: Optional[str] = None,
        ref_set_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve hotspots from the model

        For an introduction to the hotspots Enrichment,
        see http://docs.arthur.ai/user-guide/walkthroughs/enrichments.html#hotspots

        :param metric: accuracy metric used to filter hotspots tree by, defaults to "accuracy"
        :param threshold: threshold for of performance metric used for filtering hotspots, defaults to 0.5
        :param batch_id: string id for the batch to find hotspots in, defaults to None
        :param date: string used to define date, defaults to None
        :param ref_set_id: string id for the reference set to find hotspots in, defaults to None
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: raw_data read
        """
        data_param_count = sum(
            (batch_id is not None, date is not None, ref_set_id is not None)
        )
        if data_param_count != 1:
            raise ArthurUserError(
                f"Exactly one of batch_id/date/ref_set_id must be specified, {data_param_count} were provided"
            )

        endpoint = f"/models/{self.id}/enrichments/hotspots/find"
        query_params = {"metric": metric, "threshold": threshold}
        if batch_id is not None:
            query_params["batch_id"] = batch_id
        if date is not None:
            query_params["date"] = date
        if ref_set_id is not None:
            query_params["ref_set_id"] = ref_set_id

        resp = self._client.get(endpoint, params=query_params, return_raw_response=True)
        validation.validate_response_status(resp, expected_status_code=HTTPStatus.OK)

        return resp.json()

    def _update_client(self, client: HTTPClient) -> None:
        """
        Internally updates the model's ArthurAI client.

        :param client: :class:`arthurai.client.Client` object which manages data storage.
        :returns: None.
        """
        self._client = client


@dataclass
class ArthurModelGroup(ArthurBaseJsonDataclass):
    """
    (BETA) The ArthurModelGroup class is a collection of the metadata which represents a group of
    models within a Model Group on the Arthur platform.

    :param id: The auto-generated unique UUID for the model. Will be overwritten if set by the user.
    :param name: An optional display name for the model.
    :param description: An optional description of the model.
    :param archived: Indicates whether or not a model has been archived, defaults to False.
    :param created_at: UTC timestamp in ISO8601 format of when the model was created. Will be overwritten if set by the user.
    :param updated_at: UTC timestamp in ISO8601 format of when the model was last updated. Will be overwritten if set by the user.
    :param client: :class:`arthurai.client.Client` object which manages data storage
    """

    id: Optional[str] = None
    name: Optional[str] = None
    _name: Optional[str] = field(init=False, repr=False)
    description: Optional[str] = None
    _description: Optional[str] = field(init=False, repr=False)
    archived: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    # Private boolean to implement name, description setters accessing the client
    _initialized: bool = field(init=False, repr=False, default=False)

    # InitVars to be passed into __post_init__ for private storage
    client: InitVar[Optional[HTTPClient]] = None

    def __post_init__(self, client: HTTPClient) -> None:
        """
        Special initialization method for dataclasses that is called after the generated __init__() method.

        Input parameters to __post_init__ (may) be parsed out of the class variables and into this
        method. E.g. defining ArthurModel.client allows you to create an ArthurModel instance as
        `ArthurModel(client=...)` where client is only passed into __post_init__ and does not show
        up as an instance variable. To do so, the class variable type must be defined with an
        InitVar[] wrapper (refer to link to Python docs below).
        https://docs.python.org/3/library/dataclasses.html#init-only-variables

        Variables created here will only be accessible directly on the object itself, they will not
        be in the result of object.to_dict() even if marked as public (does not have preceding
        underscore).
        """
        self._client = client
        self._initialized = True

    @property  # type: ignore
    def name(self) -> Optional[str]:
        """
        (BETA) Property getter for the ArthurModelGroup's name.

        :returns: String name if one has been set, else None.
        """
        if self._name is not None and not isinstance(self._name, str):
            self._name = None
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        (BETA) Property setter for the ArthurModelGroup's name.
        Will also update the name of the corresponding model group on the Arthur platform.

        :param new: String new name to set.
        :returns: None.
        :permissions: model_group write
        """
        if self._initialized:
            if new_name is None or new_name == "":
                raise UserValueError("Cannot set name to None.")
            endpoint = f"/model_groups/{self.id}"
            self._client.patch(
                endpoint,
                json={"name": new_name},
                return_raw_response=True,
                validation_response_code=HTTPStatus.OK,
            )
        self._name = new_name

    @property  # type: ignore
    def description(self) -> Optional[str]:
        """
        (BETA) Property getter for the ArthurModelGroup's description.

        :returns: String description if one has been set, else None.
        """
        if self._description is not None and not isinstance(self._description, str):
            self._description = None
        return self._description

    @description.setter
    def description(self, new_description: str) -> None:
        """
        (BETA) Property setter for the ArthurModelGroup's description.
        Will also update the description of the corresponding model group on the Arthur platform.

        :param new: String new description to set.
        :returns: None.
        :permissions: model_group write
        """
        if self._initialized:
            if new_description is None or new_description == "":
                raise UserValueError("Cannot set description to None.")
            endpoint = f"/model_groups/{self.id}"
            self._client.patch(
                endpoint,
                json={"description": new_description},
                return_raw_response=True,
                validation_response_code=HTTPStatus.OK,
            )
        self._description = new_description

    def add_version(self, model: ArthurModel, label: Optional[str] = None) -> None:
        """
        (BETA) Adds an unsaved ArthurModel as a version of this model group by setting the
        model_group_id of the ArthurModel.

        :param model: ArthurModel object to add to this model group.
        :param label: Optional string label to apply to this model.
        :returns: None.

        :raises UserValueError: If neither sequence_num nor label are provided, or if both are.
        """
        if model.model_group_id is not None:
            raise UserValueError(
                "Model has already been saved as a version of a model group."
            )
        if label is not None:
            model.version_label = label
        model.model_group_id = self.id

    @arthur_excepted("failed to retrieve model")
    def get_version(
        self,
        sequence_num: Optional[int] = None,
        label: Optional[str] = None,
        include_archived: bool = False,
    ) -> ArthurModel:
        """
        (BETA) Retrieves a saved model within the model group that matches the unique target
        sequence_num or label, but not both. Exactly one or the other must be provided.

        :param sequence_num: `version_sequence_num` of the model version to retrieve from the group. Required if label is not specified.
        :param label: `version_label` of the model version to retrieve from the group. Required if sequence_num is not specified.
        :returns: ArthurModel if a model exists that fits the search parameters.

        :raises UserValueError: If neither sequence_num nor label are provided, or if both are.
        :raises UserTypeError: If the provided query parameter is not of the expected type.
        :raises ResponseClientError: If no such version exists within the model group.
                                     e.g. 404 Not Found: {'error': 'record not found'}
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: model_group read
        """
        if sequence_num is not None and not isinstance(sequence_num, int):
            raise UserTypeError("sequence_num must be of type int.")
        if label is not None and not isinstance(label, str):
            raise UserTypeError("label must be of type string.")
        if not isinstance(include_archived, bool):
            raise UserTypeError("include_archived must be of type bool.")

        query_params: Dict[str, Union[str, int, bool]] = {"expand": "attributes"}
        if sequence_num is not None and label is not None:
            raise UserValueError(
                "Cannot specify both sequence_num and label - \
                must specify only one."
            )
        elif sequence_num is not None:
            query_params["sequence_num"] = sequence_num
        elif label is not None:
            query_params["label"] = label
        else:
            raise UserValueError("Must specify either a sequence_num or a label.")

        if include_archived is not None:
            query_params["include_archived"] = include_archived
        resp = self._client.get(
            f"/model_groups/{self.id}/versions",
            params=query_params,
            validation_response_code=HTTPStatus.OK,
        )

        model = ArthurModel.from_dict(resp["data"][0])
        model._update_client(self._client)
        return model

    def get_versions(self, include_archived: bool = False) -> List[ArthurModel]:
        """
        (BETA) Retrieve all saved model versions from the model group as a list of ArthurModels.
        This will only return models already onboarded to the Arthur platform.

        :param include_archived: By default, only unarchived models will be retrieved, but if include_archived
                                 is True, all models from the group (archived or not) will be retrieved.
        :returns: List of all model versions saved to the Arthur platform.
        :permissions: model_group read
        """
        # TODO: use a generator instead of setting the page size to be really high
        query_params = {"page_size": 2**31 - 1, "expand": "attributes"}
        if include_archived:
            query_params["include_archived"] = include_archived
        resp = self._client.get(
            f"/model_groups/{self.id}/versions",
            params=query_params,
            validation_response_code=HTTPStatus.OK,
        )
        resp_data = resp["data"]

        model_versions_list = []
        for model_dict in resp_data:
            model = ArthurModel.from_dict(model_dict)
            model._update_client(self._client)
            model_versions_list.append(model)
        return model_versions_list

    def get_latest_version(self, include_archived: bool = False) -> ArthurModel:
        """
        (BETA) Retrieves the ArthurModel marked as the latest saved version of this model group.

        :param include_archived: By default, only unarchived models will be retrieved, but if include_archived
                                 is True, all models from the group (archived or not) will be retrieved.
        :returns: Latest ArthurModel saved as version of this model group.
        :permissions: model_group read
        """
        query_params: Dict[str, Union[str, int, bool]] = {"expand": "attributes"}
        if include_archived is not None:
            query_params["include_archived"] = include_archived
        resp = self._client.get(
            f"/model_groups/{self.id}/versions/latest",
            params=query_params,
            validation_response_code=HTTPStatus.OK,
        )
        model = ArthurModel.from_dict(resp)
        model._update_client(self._client)
        return model

    def _update_client(self, client: HTTPClient) -> None:
        """
        (BETA) Internally updates the model group's ArthurAI client.

        :param client: :class:`arthurai.client.Client` object which manages data storage.
        :returns: None.
        """
        self._client = client

    @staticmethod
    def _get_model_group(identifier: str, client: HTTPClient) -> "ArthurModelGroup":
        """
        (BETA) Retrieve an existing model group by id

        :param: identifier: Id to get the model group by

        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        """
        endpoint = f"/model_groups/{identifier}"

        resp = client.get(
            endpoint, return_raw_response=True, validation_response_code=HTTPStatus.OK
        )

        model_group = ArthurModelGroup.from_dict(resp.json())
        model_group._update_client(client)
        return model_group

    # BETA: viz allows us to use the Data visualizer to compare model metrics and drift. This is pretty hacked together
    # and will likely need a big refactor in the future.
    def viz(
        self,
        sequence_nums: Optional[List[int]] = None,
        labels: Optional[List[str]] = None,
    ) -> DataVisualizer:
        """
        (BETA) Returns a DataVisualizer object for the model versions in the group. A subset of model versions can
        be specified with a list of version sequence nums or version labels, but both cannot be specified as an
        exception will be raised.

        :param sequence_nums: Specific version sequence nums to specify a subset of model versions in the group.
        :param labels: Specific version labels to specify a subset of model versions in the group.
        :returns: DataVisualizer for models specified.
        """
        models = self._retrieve_specified_saved_model_versions(sequence_nums, labels)
        return DataVisualizer(models)

    def _retrieve_specified_saved_model_versions(
        self,
        sequence_nums: Optional[List[int]] = None,
        labels: Optional[List[str]] = None,
    ) -> List[ArthurModel]:
        """
        (BETA) Retrieves a list of model versions based on what was specified. A subset of model versions can
        be specified with a list of version sequence nums or version labels, but both cannot be specified as an
        exception will be raised.  Not specifying sequence nums or labels will return all of the saved versions in
        reverse order of their sequence_num. If sequence_nums or labels are specified, the models will be returned in
        the order given.

        :param sequence_nums: Specific version sequence nums to specify a subset of model versions in the group.
        :param labels: Specific version labels to specify a subset of model versions in the group.
        :returns: List of ArthurModels in the group.

        :raises UserValueError: When both not None sequence_nums and labels are provided.
        """
        models = []
        if sequence_nums is not None and labels is not None:
            raise UserValueError(
                "Cannot specify both sequence_nums and labels. Only one may be specified."
            )
        elif sequence_nums is not None:
            for sequence_num in sequence_nums:
                models.append(self.get_version(sequence_num=sequence_num))
        elif labels is not None:
            for label in labels:
                models.append(self.get_version(label=label))
        else:
            # sequence_nums is None and labels is None:
            models = self.get_versions()
        return models

    @arthur_excepted("failed to archive model_group")
    def archive(self) -> None:
        """
        (BETA) Calls the endpoint to archive the model group and all of its models async with a DELETE request.
        The request can still fail async if one of the models in the group cannot be deleted.

        :return: None
        :raises Exception: the model group has no ID or the model group archive request was not accepted
        :permissions: model_group delete
        """

        endpoint = f"/model_groups/{self.id}"
        # This endpoint archives each model in the group async, then archives the model_group iff all the models were
        # successfully archived.  If a model is not successfully archived, an error will be logged, but not returned
        # to the user and the model_group will not be archived.
        self._client.delete(
            endpoint,
            return_raw_response=True,
            validation_response_code=HTTPStatus.ACCEPTED,
        )
