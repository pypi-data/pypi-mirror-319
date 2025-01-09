import pytest
import pandas as pd
from arthurai import ArthurAttribute, ArthurModel
from arthurai.common.constants import InputType, OutputType, ValueType, Stage
from arthurai.core.attributes import AttributeCategory
from tests.fixtures.models.multiclass import DOG_PRED, CAT_PRED, GROUND_TRUTH, UNLINKED_CAT_PRED, UNLINKED_DOG_PRED


INPUT_TEXT = ["hello there", "hi", "what's up", "yo", "cool", "cool beans", "this", "should", "be", "unique", "yay"]
NLP_DATAFRAME = pd.DataFrame({"input_text": INPUT_TEXT,
                              "pred": [90, 80, 50, 31, 26, 18, 90, 80, 50, 31, 26],
                              "gt": [95, 81, 42, 30, 30, 27, 95, 81, 42, 30, 30]})


DOG_CLASS_STRING = "dog class"
CAT_CLASS_STRING = "cat_class"
NLP_CLASSIFICATION_DATAFRAME = pd.DataFrame({"input_text": INPUT_TEXT,
                                             DOG_PRED: [0.6, 0.8, 0.2, 0.45, 0.94, 0.12, 0.6, 0.8, 0.2, 0.45, 0.94],
                                             CAT_PRED: [0.4, 0.2, 0.8, 0.65, 0.06, 0.88, 0.4, 0.2, 0.8, 0.65, 0.06],
                                             GROUND_TRUTH: [DOG_CLASS_STRING, CAT_CLASS_STRING, DOG_CLASS_STRING, CAT_CLASS_STRING,
                                                            CAT_CLASS_STRING, DOG_CLASS_STRING, DOG_CLASS_STRING, CAT_CLASS_STRING,
                                                            DOG_CLASS_STRING, CAT_CLASS_STRING,CAT_CLASS_STRING]})

INPUT_TEXT_ATTR = ArthurAttribute(name='input_text',
                                  value_type=ValueType.Unstructured_Text,
                                  stage=Stage.ModelPipelineInput,
                                  # TODO: this seems like it should be false,
                                  #  but check that this field isn't used somewhere else where it needs to be true
                                  categorical=True,
                                  position=0,
                                  is_unique=True)

OUTPUT_TEXT_ATTR = ArthurAttribute(name='output_text',
                                   value_type=ValueType.Unstructured_Text,
                                   stage=Stage.PredictedValue,
                                   categorical=True,
                                   position=0,
                                   is_unique=False)

OUTPUT_TEXT_ATTR_LINKED = ArthurAttribute(name='output_text',
                                          value_type=ValueType.Unstructured_Text,
                                          stage=Stage.PredictedValue,
                                          categorical=True,
                                          position=0,
                                          is_unique=False,
                                          token_attribute_link="output_tokens")

OUTPUT_TOKENS_ATTR = ArthurAttribute(name='output_tokens',
                                     value_type=ValueType.Tokens,
                                     stage=Stage.PredictedValue,
                                     categorical=False,
                                     position=1,
                                     is_unique=False,
                                     token_attribute_link="output_text")

OUTPUT_PROBS_ATTR = ArthurAttribute(name='output_probs',
                                    value_type=ValueType.TokenLikelihoods,
                                    stage=Stage.PredictedValue,
                                    categorical=False,
                                    position=2,
                                    is_unique=False)

GT_STRING_ATTR = ArthurAttribute(name=GROUND_TRUTH,
                                 value_type=ValueType.String,
                                 stage=Stage.GroundTruthClass,
                                 categorical=True,
                                 categories=[AttributeCategory(value=DOG_CLASS_STRING),
                                             AttributeCategory(value=CAT_CLASS_STRING)],
                                 position=0)

GT_TEXT_ATTR = ArthurAttribute(name='gt_text',
                               value_type=ValueType.Unstructured_Text,
                               stage=Stage.GroundTruth,
                               categorical=True,
                               position=0,
                               is_unique=True,
                               token_attribute_link="gt_tokens")

GT_TOKENS_ATTR = ArthurAttribute(name='gt_tokens',
                                 value_type=ValueType.Tokens,
                                 stage=Stage.GroundTruth,
                                 categorical=False,
                                 position=1,
                                 is_unique=False,
                                 token_attribute_link="gt_text")

CLASSIFICATION_MODEL_ATTRIBUTES = [UNLINKED_CAT_PRED, UNLINKED_DOG_PRED, INPUT_TEXT_ATTR, GT_STRING_ATTR]
SEQUENCE_MODEL_ATTRIBUTES = [INPUT_TEXT_ATTR, OUTPUT_TEXT_ATTR]
SEQUENCE_MODEL_WITH_PROBS_ATTRIBUTES = [INPUT_TEXT_ATTR, OUTPUT_TEXT_ATTR_LINKED, OUTPUT_TOKENS_ATTR, OUTPUT_PROBS_ATTR]
SEQUENCE_MODEL_WITH_GT_ATTRIBUTES = [INPUT_TEXT_ATTR, OUTPUT_TEXT_ATTR, GT_TEXT_ATTR, GT_TOKENS_ATTR]

UNINITIALIZED_MODEL_DATA = {"partner_model_id": "test",
                            "client": None,
                            "input_type": InputType.NLP}


@pytest.fixture
def initial_nlp_regression_model():
    return ArthurModel(
        **UNINITIALIZED_MODEL_DATA,
        output_type=OutputType.Regression
    )


@pytest.fixture
def initial_nlp_classification_model():
    return ArthurModel(
        **UNINITIALIZED_MODEL_DATA,
        output_type=OutputType.Multiclass
    )


@pytest.fixture
def initial_nlp_sequence_model():
    return ArthurModel(
        **UNINITIALIZED_MODEL_DATA,
        output_type=OutputType.TokenSequence
    )
