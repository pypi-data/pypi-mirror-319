import datetime
import json

import pytest

from arthurai.client.http.requests import HTTPClient, requests
from arthurai.common.exceptions import ArthurUserError
from arthurai.core.alerts import AlertRule, AlertRuleBound, AlertRuleSeverity, validate_parameters_for_alert
from arthurai.core.models import ArthurModel
from tests import MockResponse

alert_rule_object = AlertRule(
    bound=AlertRuleBound.Upper,
    threshold=0.5,
    metric_id="4e18df3d-307d-4b3f-aba4-a434ca893c8a",
    severity=AlertRuleSeverity.Warning,
    metric_parameters={
        "classifier_threshold": 0.5,
        "predicted_property": "prediction"
    },
    filters=[
        {
            "property": "AGE",
            "comparator": "eq",
            "value": 22
        }
    ]
)

alert_rule_dict = {
    "bound": "upper",
    "threshold": 0.5,
    "metric_id": "4e18df3d-307d-4b3f-aba4-a434ca893c8a",
    "severity": "warning",
    "metric_parameters": {
        "classifier_threshold": 0.5,
        "predicted_property": "prediction"
    },
    "filters": [
        {
            "property": "AGE",
            "comparator": "eq",
            "value": 22
        }
    ]
}


def patch_alert_rule_post(*args, **kwargs):
    alert_rule_dict["enabled"] = True  # enabled is not a param to the alert rule creation function but defaults to True
    assert kwargs['json'] == alert_rule_dict
    alert_rule_object.id = "8c298d3f-eb38-47d2-85db-182a92a84af3"
    return MockResponse(alert_rule_object, 200)


def patch_alert_rule_post_api_version(*args, **kwargs):
    # asserting that the api_version is v3 (default)
    assert "/api/v3/" in args[2]

    alert_rule_dict["enabled"] = True  # enabled is not a param to the alert rule creation function but defaults to True
    assert json.loads(kwargs['data']) == alert_rule_dict
    alert_rule_object.id = "8c298d3f-eb38-47d2-85db-182a92a84af3"

    # adding required fields to the mock response
    mock_response = MockResponse(alert_rule_object, 200)
    mock_response.elapsed = datetime.timedelta(seconds=2.0)
    mock_response.url = ""
    mock_response.headers = {}
    mock_response._content = {}
    return mock_response


def path_alert_rule_get(*args, **kwargs):
    alert_rule_list = {
        "data": [
            {
                "name": "Lower Bound for Total Inference Count By Class - Dog",
                "metric_id": "e14e6aac-0c94-4a78-a104-871f70b8b476",
                "threshold": 200,
                "bound": "lower",
                "severity": "warning",
                "lookback_period": 360,
                "subsequent_alert_wait_time": 720,
                "enabled": True,
                "id": "2905da23-fa72-4299-92d6-40007d3a2a03",
                "metric_name": "Total Inference Count By Class - Dog",
                "attribute_name": "dog",
                "metric_parameters": {
                    "predicted_class": "dog"
                }
            },
            {
                "name": "Lower Bound for Total Inference Count By Class - Dog",
                "metric_id": "e14e6aac-0c94-4a78-a104-871f70b8b476",
                "threshold": 200,
                "bound": "lower",
                "severity": "warning",
                "lookback_period": 360,
                "subsequent_alert_wait_time": 720,
                "enabled": True,
                "id": "2905da23-fa72-4299-92d6-40007d3a2a03",
                "metric_name": "Total Inference Count By Class - Dog",
                "attribute_name": "dog"
            }
        ],
        "page": 1,
        "page_size": 20,
        "total_pages": 1,
        "total_count": 1
    }
    return MockResponse(alert_rule_list, 200)


def empty_alert_rule_get(*args, **kwargs):
    alert_rule_list = {
        "data": [],
        "page": 1,
        "page_size": 20,
        "total_pages": 1,
        "total_count": 0
    }
    return MockResponse(alert_rule_list, 200)


def null_alert_rule_get(*args, **kwargs):
    alert_rule_list = {
        "data": None,
        "page": 1,
        "page_size": 20,
        "total_pages": 1,
        "total_count": 0
    }
    return MockResponse(alert_rule_list, 200)


def patch_alert_rule_patch(*args, **kwargs):
    alert_rule_dict["id"] = "123456789"
    return MockResponse(alert_rule_dict, 200)


class TestAlertRule:

    def test_alert_rule_create(self, monkeypatch, mock_cred_env_vars, binary_classification_model: ArthurModel):
        # test successful creation of alert rule
        monkeypatch.setattr(HTTPClient, "post", patch_alert_rule_post)
        res = binary_classification_model.create_alert_rule(**alert_rule_dict)
        assert res == alert_rule_object

    def test_alert_rule_create_api_version(self, monkeypatch, mock_cred_env_vars, binary_classification_model: ArthurModel):
        # test successful creation of alert rule along with assertions for the api version

        # removing the enabled field from the alert rule dict as it is not a param to the alert rule creation function
        alert_rule_dict.pop("enabled")
        monkeypatch.setattr(requests.Session, "request", patch_alert_rule_post_api_version)
        res = binary_classification_model.create_alert_rule(**alert_rule_dict)
        assert res == alert_rule_object

    def test_get_alert_rules(self, monkeypatch, mock_cred_env_vars, binary_classification_model: ArthurModel):
        # Get existing alert rules
        monkeypatch.setattr(HTTPClient, "get", path_alert_rule_get)
        res = binary_classification_model.get_alert_rules()
        assert len(res) == 2
        for alert_rule in res:
            assert isinstance(alert_rule, AlertRule)

        # Get empty list of alert rules
        monkeypatch.setattr(HTTPClient, "get", empty_alert_rule_get)
        res = binary_classification_model.get_alert_rules()
        assert len(res) == 0
        for alert_rule in res:
            assert isinstance(alert_rule, AlertRule)

        # Get list of alert rules but the response data is null (OBS-643)
        monkeypatch.setattr(HTTPClient, "get", null_alert_rule_get)
        res = binary_classification_model.get_alert_rules()
        assert len(res) == 0
        for alert_rule in res:
            assert isinstance(alert_rule, AlertRule)

    def test_alert_rule_patch(self, monkeypatch, mock_cred_env_vars, binary_classification_model: ArthurModel):
        # test updating alert rule passing id separately
        monkeypatch.setattr(HTTPClient, "patch", patch_alert_rule_patch)
        res = binary_classification_model.update_alert_rule(alert_rule_object, "123456789")
        alert_rule_object.id = "123456789"
        assert res == alert_rule_object

        # test creating alert rule using an AlertRule object
        res = binary_classification_model.update_alert_rule(alert_rule=alert_rule_object)
        alert_rule_object.id = "123456789"
        assert res == alert_rule_object

        # ensure an error is thrown if an alert rule id is not provided
        alert_rule_object.id = None
        with pytest.raises(Exception) as context:
            binary_classification_model.update_alert_rule(alert_rule_object)

        assert "alert_rule_to_update must have a valid id" in context.value.args[0]

    @pytest.mark.parametrize('metric_parameters, expected_parameters, expected_error', [
        (
                {"classifier_threshold": 0.5, "predicted_property": "prediction"},
                {"classifier_threshold": 0.5, "predicted_property": "prediction"},
                False
        ),
        (
                {"classifier_threshold": 0.5, "predicted_property": ["prediction", "prediction2"]},
                None,
                True
        ),
        (
                {"classifier_threshold": 0.5, "predicted_property": ["prediction"]},
                {"classifier_threshold": 0.5, "predicted_property": "prediction"},
                False
        ),
        (
                None,
                {},
                False
        )
    ], ids=['valid_params', 'invalid_params', 'nested_valid_params', 'null params'])
    def test_validate_parameters_for_alert(self, metric_parameters, expected_parameters, expected_error):
        if expected_error:
            with pytest.raises(ArthurUserError):
                _ = validate_parameters_for_alert(metric_parameters)
        else:
            validated_parameters = validate_parameters_for_alert(metric_parameters)
            assert validated_parameters == expected_parameters
