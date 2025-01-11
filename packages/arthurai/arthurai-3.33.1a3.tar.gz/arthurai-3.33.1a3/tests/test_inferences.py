import json
from copy import deepcopy
from datetime import datetime, timezone
from typing import Any, Dict, List, NamedTuple, Tuple
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
import pytz
import responses
from dateutil.parser import isoparse

from arthurai import util as arthur_util, ArthurAttribute
from arthurai.common.constants import ValueType, Stage, InferenceType, TimestampInferenceType
from arthurai.common.exceptions import UserValueError
from arthurai.core.models import ArthurModel
# noinspection PyUnresolvedReferences
from tests.fixtures.mocks import client
# noinspection PyUnresolvedReferences
from tests.fixtures.models.multiclass import biclass_model
# noinspection PyUnresolvedReferences
from tests.fixtures.models.regression import FLOAT_NONINPUT, GROUND_TRUTH, INT_INPUT, PRED, batch_model
from tests.helpers import MockDatetime, MockShortUUID, assert_kwargs_equal, mock_patch, mock_post

# FIXTURES
INT_INPUT_VAL_1 = 1
INT_INPUT_VAL_2 = 2
FLOAT_INPUT_VAL_1 = 3.0
FLOAT_INPUT_VAL_2 = 4.0
PRED_VAL_1 = 5.0
PRED_VAL_2 = 10.0
GROUND_TRUTH_VAL_1 = 5.5
GROUND_TRUTH_VAL_2 = 9.5
INFERENCE_ID_1 = "inf1"
INFERENCE_ID_2 = "inf2"
TIMESTAMP_VALUE = '2021-01-21T12:00:00.123456+00:00'
BATCH_ID = 'batch_1'
BATCH_ID_2 = 'batch_2'

API_FORMAT_DATA = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_1,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
            PRED: PRED_VAL_1
        },
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_1
        },
        'batch_id': BATCH_ID
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_2,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
            PRED: PRED_VAL_2
        },
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_2
        },
        'batch_id': BATCH_ID
    }
]

API_FORMAT_DATA_NO_BATCH = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_1,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
            PRED: PRED_VAL_1
        },
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_1
        }
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_2,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
            PRED: PRED_VAL_2
        },
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_2
        }
    }
]

API_FORMAT_DATA_NO_PREDS_OR_GROUND_TRUTH = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_1,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
        },
        'batch_id': BATCH_ID
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_2,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
        },
        'batch_id': BATCH_ID
    }
]

API_FORMAT_DATA_NO_GROUND_TRUTH = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_1,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
            PRED: PRED_VAL_1
        },
        'batch_id': BATCH_ID
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_2,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
            PRED: PRED_VAL_2
        },
        'batch_id': BATCH_ID
    }
]

API_FORMAT_DATA_INFERENCES_ONLY = [
    {
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_1,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
        }
    },
    {
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_2,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
        }
    }
]

API_FORMAT_DATA_PARTIAL_GT = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_1,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
            PRED: PRED_VAL_1
        },
        'batch_id': BATCH_ID
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_2,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
            PRED: PRED_VAL_2
        },
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_2
        },
        'batch_id': BATCH_ID
    }
]

FLAT_DATA_FULL_INPUTS = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'inference_timestamp': TIMESTAMP_VALUE,
        INT_INPUT: INT_INPUT_VAL_1,
        FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
        PRED: PRED_VAL_1,
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        GROUND_TRUTH: GROUND_TRUTH_VAL_1,
        'batch_id': BATCH_ID
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'inference_timestamp': TIMESTAMP_VALUE,
        INT_INPUT: INT_INPUT_VAL_2,
        FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
        PRED: PRED_VAL_2,
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        GROUND_TRUTH: GROUND_TRUTH_VAL_2,
        'batch_id': BATCH_ID
    }
]

FLAT_DATA_NO_TIMESTAMPS_OR_IDS = [
    {
        INT_INPUT: INT_INPUT_VAL_1,
        FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
        PRED: PRED_VAL_1,
        GROUND_TRUTH: GROUND_TRUTH_VAL_1,
        'batch_id': BATCH_ID
    },
    {
        INT_INPUT: INT_INPUT_VAL_2,
        FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
        PRED: PRED_VAL_2,
        GROUND_TRUTH: GROUND_TRUTH_VAL_2,
        'batch_id': BATCH_ID
    }
]

FLAT_DATA_INFERENCES_ONLY = [
    {
        INT_INPUT: INT_INPUT_VAL_1,
        FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
        PRED: PRED_VAL_1,
    },
    {
        INT_INPUT: INT_INPUT_VAL_2,
        FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
        PRED: PRED_VAL_2,
    }
]

FLAT_DATA_PARTIAL_GT = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'inference_timestamp': TIMESTAMP_VALUE,
        INT_INPUT: INT_INPUT_VAL_1,
        FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
        PRED: PRED_VAL_1,
        'batch_id': BATCH_ID
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'inference_timestamp': TIMESTAMP_VALUE,
        INT_INPUT: INT_INPUT_VAL_2,
        FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
        PRED: PRED_VAL_2,
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        GROUND_TRUTH: GROUND_TRUTH_VAL_2,
        'batch_id': BATCH_ID
    }
]

API_FORMAT_GROUND_TRUTHS = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_1
        }
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_2
        }
    }
]

FLAT_GROUND_TRUTH_DATA_FULL_INPUTS = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        GROUND_TRUTH: GROUND_TRUTH_VAL_1
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        GROUND_TRUTH: GROUND_TRUTH_VAL_2
    }
]

FLAT_GROUND_TRUTH_DATA_NO_TIMESTAMPS = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        GROUND_TRUTH: GROUND_TRUTH_VAL_1
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        GROUND_TRUTH: GROUND_TRUTH_VAL_2
    }
]

MULTI_BATCH_DATA = [
    {
        'partner_inference_id': INFERENCE_ID_1,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_1,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_1,
            PRED: PRED_VAL_1
        },
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_1
        },
        'batch_id': BATCH_ID
    },
    {
        'partner_inference_id': INFERENCE_ID_2,
        'inference_timestamp': TIMESTAMP_VALUE,
        'inference_data': {
            INT_INPUT: INT_INPUT_VAL_2,
            FLOAT_NONINPUT: FLOAT_INPUT_VAL_2,
            PRED: PRED_VAL_2
        },
        'ground_truth_timestamp': TIMESTAMP_VALUE,
        'ground_truth_data': {
            GROUND_TRUTH: GROUND_TRUTH_VAL_2
        },
        'batch_id': BATCH_ID_2
    }
]

BATCH_COUNTS = {
    BATCH_ID: 2
}

MULTI_BATCH_COUNTS = {
    BATCH_ID: 1,
    BATCH_ID_2: 1
}

PREDS_RAW_LIST = [PRED_VAL_1, PRED_VAL_2]
GROUND_TRUTH_RAW_LIST = [GROUND_TRUTH_VAL_1, GROUND_TRUTH_VAL_2]

FULL_DATA_FRAME = pd.DataFrame(FLAT_DATA_FULL_INPUTS)
FULL_DATA_FRAME['inference_timestamp'] = pd.to_datetime(FULL_DATA_FRAME['inference_timestamp'])
FULL_DATA_FRAME['ground_truth_timestamp'] = pd.to_datetime(FULL_DATA_FRAME['ground_truth_timestamp'])

EXPECTED_RESPONSE = {
    "counts": {
        "success": 2,
        "failure": 0,
        "total": 2
    },
    "results": [
        {
            "partner_inference_id": INFERENCE_ID_1,
            "message": "success",
            "status": 200
        },
        {
            "partner_inference_id": INFERENCE_ID_2,
            "message": "success",
            "status": 200
        }
    ]
}

EXPECTED_RESPONSE_NO_IDS = {
    "counts": {
        "success": 2,
        "failure": 0,
        "total": 2
    },
    "results": [
        {
            "message": "success",
            "status": 200
        },
        {
            "message": "success",
            "status": 200
        }
    ]
}


@pytest.fixture(params=['batch_model', 'biclass_model'])
def model(request):
    return request.getfixturevalue(request.param)


class TestInferences:

    def test_format_inference_no_gt(self, client, batch_model):
        inference = batch_model._format_inference_request(
            inference_timestamp=datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
            partner_inference_id="1234",
            model_pipeline_input=ArthurModel._replace_nans_and_infinities_in_dict({"attr": 5}),
            non_input_data=ArthurModel._replace_nans_and_infinities_in_dict({"Gender": "male"}),
            predicted_value=ArthurModel._replace_nans_and_infinities_in_dict({"prediction": 800}),
            ground_truth=ArthurModel._replace_nans_and_infinities_in_dict(None)
        )

        inferences = arthur_util.format_timestamps([inference])
        assert len(inferences) == 1
        assert inferences[0]["inference_timestamp"] == "2020-08-13T17:44:31+00:00"
        assert "ground_truth_timestamp" not in inferences[0]
        assert "ground_truth" not in inferences[0]

    @responses.activate
    def test_format_inference_request(self, batch_model):
        inf = batch_model._format_inference_request(
            inference_timestamp="2020-08-13T17:44:31.552125Z",
            partner_inference_id="1234",
            model_pipeline_input={"attr": 5},
            non_input_data={"Gender": "male"},
            predicted_value={"prediction": 800},
            ground_truth={"actual_value": 812}
        )

        expected = {
            "inference_timestamp": "2020-08-13T17:44:31.552125Z",
            "partner_inference_id": "1234",
            "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
            "ground_truth_timestamp": "2020-08-13T17:44:31.552125Z",
            "ground_truth_data": {"actual_value": 812}
        }

        assert inf == expected

    def test_correct_inference_timestamps(self):
        """Test for correct timestamp formats for inferences and we return the proper strings"""
        inference_timestamps = [
            {
                "inference_timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "partner_inference_id": "1234",
                "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
                "ground_truth_timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "ground_truth_data": {"actual_value": 812}
            },
            {
                "inference_timestamp": "2020-08-13T17:44:31Z",
                "partner_inference_id": "1234",
                "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
                "ground_truth_timestamp": "2020-08-13T17:44:31+00:00",
                "ground_truth_data": {"actual_value": 812}
            }
        ]
        correct_outputs = [("2020-08-13T17:44:31+00:00", "2020-08-13T17:44:31+00:00"),
                           ("2020-08-13T17:44:31Z", "2020-08-13T17:44:31+00:00")]

        reformatted_inferences = arthur_util.format_timestamps(inference_timestamps)
        for count, inf in enumerate(reformatted_inferences):
            assert inf['inference_timestamp'] == correct_outputs[count][0]
            assert inf['ground_truth_timestamp'] == correct_outputs[count][1]

    def test_incorrect_inference_timestamps(self):
        """Test for incorrect timestamp formats for inferences and proper errors"""
        inference_timestamps = [
            {
                "inference_timestamp": datetime(2020, 8, 13, 17, 44, 31),
                "partner_inference_id": "1234",
                "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
                "ground_truth_timestamp": datetime(2020, 8, 13, 17, 44, 31),
                "ground_truth_data": {"actual_value": 812}
            },
            {
                "inference_timestamp": "2020-08-13T17:44:31Z",
                "partner_inference_id": "1234",
                "inference_data": {"attr": 5, "Gender": "male", "prediction": 800},
                "ground_truth_timestamp": "2020-08-13T17:44:31+00:00",
                "ground_truth_data": {"actual_value": 812}
            }
        ]

        with pytest.raises(ValueError):
            arthur_util.format_timestamps(inference_timestamps)

    @pytest.mark.parametrize('is_ref_data', [True, False])
    def test_format_timestamps(self, is_ref_data):
        key = InferenceType.REFERENCE_DATA if is_ref_data else InferenceType.INFERENCE_DATA
        inference_timestamps = [
            {
                TimestampInferenceType.INFERENCE_TIMESTAMP: datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                "partner_inference_id": "1234",
                key: {"timestamp_attr": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                      "time_series_attr": [{"timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                                            "value": 100}]},
                TimestampInferenceType.GROUND_TRUTH_TIMESTAMP: datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                InferenceType.GROUND_TRUTH_DATA: {"actual_value": 812}
            },
            {
                TimestampInferenceType.INFERENCE_TIMESTAMP: "2020-08-13T17:44:31Z",
                "partner_inference_id": "1234",
                key: {"timestamp_attr": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                      "time_series_attr": [{"timestamp": datetime(2020, 8, 13, 17, 44, 31, tzinfo=timezone.utc),
                                            "value": 100}]},
                TimestampInferenceType.GROUND_TRUTH_TIMESTAMP: "2020-08-13T17:44:31+00:00",
                InferenceType.GROUND_TRUTH_DATA: {"actual_value": 812}
            }
        ]

        correct_outputs = [("2020-08-13T17:44:31+00:00", "2020-08-13T17:44:31+00:00",
                            {"timestamp_attr": "2020-08-13T17:44:31+00:00",
                             "time_series_attr": [{"timestamp": "2020-08-13T17:44:31+00:00", "value": 100}]}),
                           ("2020-08-13T17:44:31Z", "2020-08-13T17:44:31+00:00",
                           {"timestamp_attr": "2020-08-13T17:44:31+00:00",
                            "time_series_attr": [{"timestamp": "2020-08-13T17:44:31+00:00", "value": 100}]})
                           ]

        reformatted_inferences = arthur_util.format_timestamps(inference_timestamps, None,
                                                               ["timestamp_attr"], ["time_series_attr"], is_ref_data)
        for count, inf in enumerate(reformatted_inferences):
            assert inf[TimestampInferenceType.INFERENCE_TIMESTAMP] == correct_outputs[count][0]
            assert inf[TimestampInferenceType.GROUND_TRUTH_TIMESTAMP] == correct_outputs[count][1]
            assert inf[key] == correct_outputs[count][2]

    @pytest.mark.parametrize('inference, expected_inf, expected_err, is_ref_data', [
        ({InferenceType.INFERENCE_DATA: {"bill_pay_history": [{"timestamp": datetime(2000, 10, 29, 0, 0, 0, 0, pytz.UTC),
                                                               "value": 1},
                                                              {"timestamp": datetime(1999, 2, 22, 0, 0, 0, 0, pytz.UTC),
                                                               "value": 2}]}},
         {"bill_pay_history": [{"timestamp": datetime(2000, 10, 29, 0, 0, 0, 0, pytz.UTC).isoformat(), "value": 1},
                                {"timestamp": datetime(1999, 2, 22, 0, 0, 0, 0, pytz.UTC).isoformat(), "value": 2}]},
         None, False),  # happy path inference data
        ({"bill_pay_history": [{"timestamp": datetime(2000, 10, 29, 0, 0, 0, 0, pytz.UTC), "value": 1}]}, None,
         UserValueError, False),  # test missing inference_data field
        ({InferenceType.INFERENCE_DATA: {"bill_pay_history": [{"value": 1}]}},
         {"bill_pay_history": [{"value": 1}]}, None, False),  # test missing timestamp field doesn't error
        ({InferenceType.INFERENCE_DATA: {"value": 1}}, {"value": 1}, None, False),  # test missing attribute data doesn't error
        ({InferenceType.REFERENCE_DATA: {"bill_pay_history": [{"timestamp": datetime(2000, 10, 29, 0, 0, 0, 0, pytz.UTC),
                                                               "value": 1},
                                                              {"timestamp": datetime(1999, 2, 22, 0, 0, 0, 0, pytz.UTC),
                                                               "value": 2}]}},
         {"bill_pay_history": [{"timestamp": datetime(2000, 10, 29, 0, 0, 0, 0, pytz.UTC).isoformat(), "value": 1},
                               {"timestamp": datetime(1999, 2, 22, 0, 0, 0, 0, pytz.UTC).isoformat(), "value": 2}]},
         None, True)  # happy path reference data
    ])
    def test_format_time_series_attr_timestamps(self, inference, expected_inf, expected_err, is_ref_data):
        time_series_attributes = ["bill_pay_history"]
        if expected_err is None:
            assert arthur_util.format_time_series_attr_timestamps(inference, time_series_attributes,
                                                                  is_reference_data=is_ref_data) == expected_inf
        else:
            with pytest.raises(expected_err):
                arthur_util.format_time_series_attr_timestamps(inference, time_series_attributes,
                                                               is_reference_data=is_ref_data)

    def test_format_timestamp_with_location(self):
        unaware_timestamp = datetime(2021, 2, 8, 12, 10, 5)
        assert arthur_util.format_timestamp(unaware_timestamp, "America/Phoenix") == "2021-02-08T19:10:05+00:00"

    # this is actually more generic but leaving scoped this way for now
    class InferencesCase(NamedTuple):
        pos_args: Tuple
        kwargs: Dict[str, Any]
        expected_request: List[Dict[str, Any]]
        expected_response: Dict[str, Any]
        batch_counts: Dict[str, int] = {}

    send_inferences_cases = [
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': API_FORMAT_DATA}, expected_request=API_FORMAT_DATA,
            expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS), id="orig-api-format"),
        pytest.param(InferencesCase(
            pos_args=(API_FORMAT_DATA,), kwargs={}, expected_request=API_FORMAT_DATA,
            expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS), id="orig-api-format-positional"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': API_FORMAT_DATA_NO_PREDS_OR_GROUND_TRUTH, 'predictions': PREDS_RAW_LIST,
                                 'ground_truths': GROUND_TRUTH_RAW_LIST},
            expected_request=API_FORMAT_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="api-format-with-preds-and-gt-separate-no-gt-timestamps"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': API_FORMAT_DATA_NO_PREDS_OR_GROUND_TRUTH,
                                 'predictions': PREDS_RAW_LIST},
            expected_request=API_FORMAT_DATA_NO_GROUND_TRUTH, expected_response=EXPECTED_RESPONSE,
            batch_counts=BATCH_COUNTS), id="api-format-no-ground-truth"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': FLAT_DATA_FULL_INPUTS}, expected_request=API_FORMAT_DATA,
            expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS), id="flat-dict-format"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': FLAT_DATA_INFERENCES_ONLY,
                                 'predictions': PREDS_RAW_LIST,
                                 'ground_truths': GROUND_TRUTH_RAW_LIST,
                                 'batch_id': BATCH_ID},
            expected_request=API_FORMAT_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="flat-dict-format-separate-preds-gt"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': FLAT_DATA_INFERENCES_ONLY,
                                 'predictions': PREDS_RAW_LIST,
                                 'ground_truths': GROUND_TRUTH_RAW_LIST},
            expected_request=API_FORMAT_DATA_NO_BATCH, expected_response=EXPECTED_RESPONSE, batch_counts={}),
            id="flat-dict-format-separate-preds-gt-no-batch"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': FLAT_DATA_PARTIAL_GT,
                                 'batch_id': BATCH_ID},
            expected_request=API_FORMAT_DATA_PARTIAL_GT, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="flat-dict-format-partial-gt"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': pd.DataFrame(FLAT_DATA_INFERENCES_ONLY),
                                 'predictions': pd.Series(PREDS_RAW_LIST),
                                 'ground_truths': np.array(GROUND_TRUTH_RAW_LIST),
                                 'batch_id': BATCH_ID},
            expected_request=API_FORMAT_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="mixed-types"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': FULL_DATA_FRAME},
            expected_request=API_FORMAT_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="single-data-frame"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': pd.DataFrame(FLAT_DATA_INFERENCES_ONLY),
                                 'predictions': pd.DataFrame({PRED: PREDS_RAW_LIST}),
                                 'ground_truths': pd.DataFrame({GROUND_TRUTH: GROUND_TRUTH_RAW_LIST}),
                                 'batch_id': BATCH_ID},
            expected_request=API_FORMAT_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="three-dataframes"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': FLAT_DATA_NO_TIMESTAMPS_OR_IDS,
                                 'batch_id': BATCH_ID,
                                 'inference_timestamps': [TIMESTAMP_VALUE, TIMESTAMP_VALUE],
                                 'ground_truth_timestamps': [TIMESTAMP_VALUE, TIMESTAMP_VALUE],
                                 'partner_inference_ids': [INFERENCE_ID_1, INFERENCE_ID_2]},
            expected_request=API_FORMAT_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="timestamps-and-ids-separate"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': FLAT_DATA_NO_TIMESTAMPS_OR_IDS,
                                 'batch_id': BATCH_ID,
                                 'inference_timestamps': pd.Series([TIMESTAMP_VALUE, TIMESTAMP_VALUE]),
                                 'ground_truth_timestamps': pd.Series([TIMESTAMP_VALUE, TIMESTAMP_VALUE]),
                                 'partner_inference_ids': pd.Series([INFERENCE_ID_1, INFERENCE_ID_2])},
            expected_request=API_FORMAT_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="timestamps-and-ids-separate-series"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': FLAT_DATA_NO_TIMESTAMPS_OR_IDS,
                                 'batch_id': BATCH_ID,
                                 'inference_timestamps': [isoparse(TIMESTAMP_VALUE),
                                                          isoparse(TIMESTAMP_VALUE)],
                                 'ground_truth_timestamps': [isoparse(TIMESTAMP_VALUE), isoparse(TIMESTAMP_VALUE)],
                                 'partner_inference_ids': [INFERENCE_ID_1, INFERENCE_ID_2]},
            expected_request=API_FORMAT_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=BATCH_COUNTS),
            id="timestamps-and-ids-separate-datetime-format"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'inferences': MULTI_BATCH_DATA},
            expected_request=MULTI_BATCH_DATA, expected_response=EXPECTED_RESPONSE, batch_counts=MULTI_BATCH_COUNTS),
            id="multi-batch"),

    ]

    @responses.activate
    @pytest.mark.parametrize("case", send_inferences_cases)
    def test_send_inferences(self, model, case: InferencesCase):
        pos_args_copy = deepcopy(case.pos_args)
        kwargs_copy = deepcopy(case.kwargs)
        model_id = model.id
        mock_post(f"/api/v3/models/{model_id}/inferences", case.expected_response, status=207)
        for batch_id in case.batch_counts.keys():
            mock_patch(f"/api/v3/models/{model_id}/batches/{batch_id}", {'status': "ok"}, status=200)
        uuid_generator = MockShortUUID([INFERENCE_ID_1, INFERENCE_ID_2])
        datetime_generator = MockDatetime([TIMESTAMP_VALUE])

        with patch("arthurai.core.models.shortuuid.uuid") as uuid_mock:
            with patch("arthurai.core.models.datetime") as datetime_mock:
                uuid_mock.side_effect = uuid_generator.next
                datetime_mock.now.side_effect = datetime_generator.next
                actual_response = model.send_inferences(*case.pos_args, **case.kwargs)

            # inputs were not modified
            assert case.pos_args == pos_args_copy
            assert_kwargs_equal(kwargs_copy, case.kwargs)

            expected_num_close_batch_calls = len(case.batch_counts) if model.is_batch else 0
            assert len(responses.calls) == 1 + expected_num_close_batch_calls
            assert responses.calls[0].request.body is not None
            assert responses.calls[0].request.body is not None

            actual_request_body = json.loads(responses.calls[0].request.body)
            assert actual_request_body == case.expected_request
            assert actual_response == case.expected_response

            # batch closed
            batch_close_calls = {}
            for call in list(responses.calls)[1:]:
                assert call.request.url is not None
                batch_close_calls[call.request.url.split("/")[-1]] = call.request.body
            if model.is_batch:
                for batch_id in case.batch_counts.keys():
                    expected_body = json.dumps({
                        "status": "uploaded",
                        "total_record_count": case.batch_counts[batch_id]
                    })
                    assert batch_close_calls[batch_id] == expected_body

    update_ground_truths_cases = [
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'ground_truths': API_FORMAT_GROUND_TRUTHS}, expected_request=API_FORMAT_GROUND_TRUTHS,
            expected_response=EXPECTED_RESPONSE_NO_IDS), id="orig-api-format"),
        pytest.param(InferencesCase(
            pos_args=(API_FORMAT_GROUND_TRUTHS,), kwargs={}, expected_request=API_FORMAT_GROUND_TRUTHS,
            expected_response=EXPECTED_RESPONSE_NO_IDS), id="orig-api-format-positional"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'ground_truths': FLAT_GROUND_TRUTH_DATA_FULL_INPUTS},
            expected_request=API_FORMAT_GROUND_TRUTHS, expected_response=EXPECTED_RESPONSE_NO_IDS),
            id="flat-dict-format"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'ground_truths': FLAT_GROUND_TRUTH_DATA_NO_TIMESTAMPS},
            expected_request=API_FORMAT_GROUND_TRUTHS, expected_response=EXPECTED_RESPONSE_NO_IDS),
            id="flat-dict-no-timestamps"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'ground_truths': GROUND_TRUTH_RAW_LIST,
                                 'partner_inference_ids': [INFERENCE_ID_1, INFERENCE_ID_2]},
            expected_request=API_FORMAT_GROUND_TRUTHS, expected_response=EXPECTED_RESPONSE_NO_IDS),
            id="single-list"),
        pytest.param(InferencesCase(
            pos_args=(), kwargs={'ground_truths': pd.DataFrame(FLAT_GROUND_TRUTH_DATA_FULL_INPUTS)},
            expected_request=API_FORMAT_GROUND_TRUTHS, expected_response=EXPECTED_RESPONSE_NO_IDS),
            id="single-dataframe")
    ]

    @responses.activate
    @pytest.mark.parametrize("case", update_ground_truths_cases)
    def test_update_ground_truth(self, model, case: InferencesCase):
        pos_args_copy = deepcopy(case.pos_args)
        kwargs_copy = deepcopy(case.kwargs)
        mock_patch(f"/api/v3/models/{model.id}/inferences", case.expected_response, status=207)
        datetime_generator = MockDatetime([TIMESTAMP_VALUE])

        with patch("arthurai.core.models.datetime") as datetime_mock:
            datetime_mock.now.side_effect = datetime_generator.next
            actual_response = model.update_inference_ground_truths(*case.pos_args, **case.kwargs)

        # inputs were not modified
        assert case.pos_args == pos_args_copy
        assert_kwargs_equal(kwargs_copy, case.kwargs)

        assert len(responses.calls) == 1
        assert responses.calls[0].request.body is not None
        actual_request_body = json.loads(responses.calls[0].request.body)

        assert actual_request_body == case.expected_request
        assert actual_response == case.expected_response
