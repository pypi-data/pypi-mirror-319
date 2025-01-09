import pytest
import responses

from arthurai import ArthurModel
from arthurai.common.constants import ModelStatus, ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE, InputType, \
    OutputType
from arthurai.common.exceptions import ArthurUnexpectedError
from arthurai.core.model_status_waiter import ModelStatusWaiter
from tests.helpers import mock_get
from tests.fixtures.models import regression as reg
from tests.fixtures.mocks import client

CREATING_STATUS_LIST = [ModelStatus.Ready, ModelStatus.CreationFailed]


def get_test_model(client):
    return ArthurModel(
        id=reg.TABULAR_MODEL_ID,
        partner_model_id="test",
        client=client.client,
        input_type=InputType.Tabular,
        output_type=OutputType.Multiclass,
    )


@responses.activate
def test_model_status_wait_creating_ready(client):
    model = get_test_model(client)
    mock_get(f"/api/v3/models/{reg.TABULAR_MODEL_ID}", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Creating
    }, status=200)
    mock_get(f"/api/v3/models/{reg.TABULAR_MODEL_ID}", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Ready
    }, status=200)

    model_status_waiter = ModelStatusWaiter(model, client=client.client)

    status = model_status_waiter.wait_for_valid_status(CREATING_STATUS_LIST, ONBOARDING_SPINNER_MESSAGE,
                                                       ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 2
    assert status == ModelStatus.Ready


@responses.activate
def test_model_status_wait_creating_failed(client):
    model = get_test_model(client)
    mock_get(f"/api/v3/models/{reg.TABULAR_MODEL_ID}", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Creating
    }, status=200)
    mock_get(f"/api/v3/models/{reg.TABULAR_MODEL_ID}", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.CreationFailed
    }, status=200)

    model_status_waiter = ModelStatusWaiter(model, client=client.client)

    status = model_status_waiter.wait_for_valid_status(CREATING_STATUS_LIST, ONBOARDING_SPINNER_MESSAGE,
                                                       ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 2
    assert status == ModelStatus.CreationFailed


@responses.activate
def test_model_status_get_model_exception(client):
    model = get_test_model(client)
    mock_get(f"/api/v3/models/{reg.TABULAR_MODEL_ID}", response_body={}, status=500)

    model_status_waiter = ModelStatusWaiter(model, client=client.client)

    with pytest.raises(ArthurUnexpectedError):
        model_status_waiter.wait_for_valid_status(CREATING_STATUS_LIST, ONBOARDING_SPINNER_MESSAGE,
                                                  ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 1
