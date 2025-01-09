import os
import re
from datetime import timedelta
from http import HTTPStatus
from unittest import mock

import pytest
from arthurai.core.models import ArthurModel
import responses

from tests import MockResponse

from arthurai import ArthurAI
from arthurai.common.constants import InputType, OutputType
from arthurai.client.validation import validate_multistatus_response_and_get_failures, validate_response_status
from arthurai.common.exceptions import ResponseServerError, ResponseClientError, ResponseRedirectError, \
    UnexpectedValueError, UserValueError
from tests.fixtures.mocks import ACCESS_KEY, BASE_URL, USER_TOKEN
from tests.helpers import mock_get, mock_post


class MockAuthRefresher:

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def refresh():
        # tell to sleep for 60 sec before refreshing
        return {'Authorization': USER_TOKEN}, timedelta(seconds=60)


class TestClient:

    def _mock_get_user(self):
        mock_get(f"/api/v3/users/me", status=HTTPStatus.OK,
                 response_body={"organization_id": "65624ee6-9a73-4fe3-a7ff-8612f7d11c21", "role": "Model Owner"})

    def _mock_get_user_unauthorized(self):
        mock_get(f"/api/v3/users/me", status=HTTPStatus.UNAUTHORIZED,
                 response_body={"bad": "user"})

    def _mock_user_login(self):
        mock_post(f"/api/v3/login", status=HTTPStatus.OK, response_body={},
                  headers={"Set-Cookie": 'Authorization=' + USER_TOKEN})

    @pytest.mark.usefixtures('mock_cred_env_vars')
    def test_client_init_env_vars(self):
        client = ArthurAI(offline=True, allow_insecure=True)
        assert client.client.base_url == 'https://mock'
        assert client.client.path_prefix == "/api/v3"
        assert client.client.session.headers.get('Authorization') == 'access_key'
        assert client.client.session.verify is False

        client = ArthurAI(url="this is a url", access_key="this is an access key", offline=True, allow_insecure=True)
        assert client.client.base_url == "https://this is a url"
        assert client.client.path_prefix == "/api/v3"
        assert client.client.session.headers.get('Authorization') == "this is an access key"
        assert client.client.session.verify is False

        client = ArthurAI(url="http://this is a url", access_key="this is an access key", offline=True, allow_insecure=True)
        assert client.client.base_url == "http://this is a url"
        assert client.client.path_prefix == "/api/v3"
        assert client.client.session.headers.get('Authorization') == "this is an access key"
        assert client.client.session.verify is False

        with pytest.raises(ValueError):
            ArthurAI(url="http://this is a url/apath", access_key="this is an access key", offline=True, allow_insecure=True)

        with pytest.raises(ValueError):
            ArthurAI(url="http://this is a url?food=good", access_key="this is an access key", offline=True, allow_insecure=True)

        with pytest.raises(ValueError):
            ArthurAI(url="fatfinger://this is a url", access_key="this is an access key", offline=True, allow_insecure=True)

        with pytest.raises(ValueError):
            ArthurAI(url="https:", access_key="this is an access key", offline=True, allow_insecure=True)

        with pytest.raises(ValueError):
            ArthurAI(url='http://asdfa', access_key='this is an access_key', allow_insecure=False)

    @pytest.mark.userfixstures('mock_login_env_vars')
    def test_client_init_access_key_overrides_env_vars(self):
        client = ArthurAI(url="http://url", access_key="this is an access key", offline=True, allow_insecure=True)
        assert client.client.session.headers.get('Authorization') == "this is an access key"

    @pytest.mark.usefixtures('mock_cred_env_vars_ssl_true')
    def test_client_init_env_vars_ssl_true(self):
        client = ArthurAI(url="http://this is a url", access_key="this is an access key", offline=True, allow_insecure=True)
        assert client.client.session.verify is True

    @pytest.mark.usefixtures('mock_cred_env_vars_ssl_garbage')
    def test_client_init_env_vars_ssl_garbage(self):
        with pytest.raises(UserValueError):
            ArthurAI(url="http://this is a url", access_key="this is an access key", offline=True)

    @responses.activate
    def test_client_init(self):
        self._mock_get_user()

        ArthurAI(access_key=ACCESS_KEY, url=BASE_URL)
        assert len(responses.calls) == 1
        expectedResponse = {'organization_id': '65624ee6-9a73-4fe3-a7ff-8612f7d11c21', 'role': 'Model Owner'}
        assert expectedResponse == responses.calls[0].response.json()

    @responses.activate
    def test_client_init_config_param(self):
        self._mock_get_user()

        ArthurAI(config={'access_key': ACCESS_KEY, 'url': BASE_URL})
        assert len(responses.calls) == 1
        expectedResponse = {'organization_id': '65624ee6-9a73-4fe3-a7ff-8612f7d11c21', 'role': 'Model Owner'}
        assert expectedResponse == responses.calls[0].response.json()

    @responses.activate
    def test_client_init_bad_host(self):
        with pytest.raises(UserValueError, match=".*please ensure the URL is correct.*"):
            ArthurAI(access_key=ACCESS_KEY, url=BASE_URL)
        assert len(responses.calls) == 1

    @responses.activate
    def test_client_init_bad_access_key(self):
        self._mock_get_user_unauthorized()
        with pytest.raises(UserValueError, match=".*please ensure your access key is correct.*"):
            ArthurAI(access_key=ACCESS_KEY, url=BASE_URL)
        assert len(responses.calls) == 1

    @mock.patch('arthurai.client.client.AuthRefresher', MockAuthRefresher)
    @responses.activate
    def test_client_login_with_username_password(self):
        self._mock_user_login()
        self._mock_get_user()

        arthur = ArthurAI(login="arthur", password="password", url=BASE_URL)
        assert USER_TOKEN == arthur.client.session.headers['Authorization']
        assert arthur.verify_ssl is True
        assert arthur.client.session.verify is True

        arthur = ArthurAI(login="arthur", password="password", url=BASE_URL, verify_ssl=False)
        assert arthur.client.session.verify is False

    @responses.activate
    def test_client_init_offline(self):
        ArthurAI(access_key=ACCESS_KEY, url=BASE_URL, offline=True)
        assert len(responses.calls) == 0

    @responses.activate
    def test_client_init_offlines(self):
        mock_get(f"/api/v3/models/1234", status=200,
                 response_body={"organization_id": "65624ee6-9a73-4fe3-a7ff-8612f7d11c21", "role": "Model Owner"})
        ArthurAI(access_key=ACCESS_KEY, url=BASE_URL, offline=True)
        assert len(responses.calls) == 0

    @mock.patch('arthurai.client.client.AuthRefresher', MockAuthRefresher)
    @responses.activate
    def test_client_sets_model_id_and_user_header(self):
        model_data = {
            "id": "1234",
            "partner_model_id": "",
            "input_type": InputType.Tabular,
            "output_type": OutputType.Regression,
            "display_name": "",
            "description": "",
            "attributes": [],
        }
        mock_get("/api/v3/models/1234", status=200, response_body=model_data)

        self._mock_get_user()

        client = ArthurAI(access_key=ACCESS_KEY, url=BASE_URL)
        client.get_model('1234')

        assert len(responses.calls) == 2
        if "models" in responses.calls[1].request.url:
            header = responses.calls[1].request.headers
        else:
            header = responses.calls[0].request.headers
        assert 'User-Agent' in header
        print(header['User-Agent'])
        assert re.findall(r"^arthur-sdk\/\d.\d+.\d|\w+ \(system=\w*\)$",
                          header['User-Agent'])
        assert os.getenv("ARTHUR_LAST_MODEL_ID") == "1234"

    @responses.activate
    def test_connection_get_model_group(self):
        model_group_id = "01234567-89ab-cdef-0123-456789abcdef"
        model_group_name = "Test Model Group"
        model_group_description = "Test Model Group Description"
        model_group_archived = False
        model_group_created_at = "2022-01-20T23:22:18.185267Z"
        model_group_updated_at = "2022-01-20T23:22:32.914068Z"

        model_group_data = {
            "id": model_group_id,
            "name": model_group_name,
            "description": model_group_description,
            "archived": model_group_archived,
            "created_at": model_group_created_at,
            "updated_at": model_group_updated_at,
            # "versions": MODEL_RESPONSE_JSON
        }

        self._mock_get_user()
        mock_get(f"/api/v3/model_groups/{model_group_id}",
                 status=HTTPStatus.OK,
                 response_body=model_group_data)

        client = ArthurAI(access_key=ACCESS_KEY, url=BASE_URL)
        model_group_from_id = client.get_model_group(model_group_id)

        model = ArthurModel(model_group_id=model_group_id, partner_model_id='pmid', input_type=InputType.Tabular,
                            output_type=OutputType.Multiclass)
        model_group_from_model = client.get_model_group(model)

        assert model_group_from_id == model_group_from_model


class TestGetMultiStatusResponseFailures:
    # fixtures
    SUCCESS_RESULTS = [{"message": "ok", "status": HTTPStatus.OK}, {"message": "created", "status": HTTPStatus.CREATED}]
    USER_FAIL_RESULTS = [{"message": "not found", "status": HTTPStatus.NOT_FOUND}]
    INTERNAL_FAIL_RESULTS = [{"message": "failure", "status": HTTPStatus.INTERNAL_SERVER_ERROR},
                             {"message": "choose", "status": HTTPStatus.MULTIPLE_CHOICES}]
    SUCCESS_BODY = {"counts": {"success": len(SUCCESS_RESULTS), "failure": 0, "total": len(SUCCESS_RESULTS)},
                    "results": SUCCESS_RESULTS}
    FAILURES_BODY = {"counts": {"success": len(SUCCESS_RESULTS),
                                "failure": len(INTERNAL_FAIL_RESULTS) + len(USER_FAIL_RESULTS),
                                "total": len(SUCCESS_RESULTS) + len(INTERNAL_FAIL_RESULTS) + len(USER_FAIL_RESULTS)},
                     "results": SUCCESS_RESULTS + USER_FAIL_RESULTS + INTERNAL_FAIL_RESULTS}
    MISMATCHED_COUNTS_BODY = {"counts": {"success": len(SUCCESS_RESULTS), "failure": 0,
                                         "total": len(SUCCESS_RESULTS)},
                              "results": SUCCESS_RESULTS + USER_FAIL_RESULTS + INTERNAL_FAIL_RESULTS}

    def test_success(self):
        response = MockResponse(self.SUCCESS_BODY, HTTPStatus.MULTI_STATUS)
        actual_user_failures, actual_internal_failures = validate_multistatus_response_and_get_failures(response)
        assert actual_user_failures == []
        assert actual_internal_failures == []

    def test_failures(self):
        response = MockResponse(self.FAILURES_BODY, HTTPStatus.MULTI_STATUS)
        actual_user_failures, actual_internal_failures = validate_multistatus_response_and_get_failures(response)
        assert actual_user_failures == self.USER_FAIL_RESULTS
        assert actual_internal_failures == self.INTERNAL_FAIL_RESULTS

    def test_bad_status(self):
        response = MockResponse(self.SUCCESS_BODY, HTTPStatus.OK)
        with pytest.raises(ValueError):
            validate_multistatus_response_and_get_failures(response)

    def test_mismatched_counts(self):
        response = MockResponse(self.MISMATCHED_COUNTS_BODY, HTTPStatus.MULTI_STATUS)
        with pytest.raises(ValueError):
            validate_multistatus_response_and_get_failures(response)


# TODO: add testing around allowed exceptions and what gets raised first (e.g. expected 207 but 404 shouldn't raise
#  UnexpectedValueError)
class TestValidateResponse:
    # fixtures
    JSON_BODY = {"status": "somestatus"}
    BYTES_BODY = b"bodybytes"

    def test_server_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.INTERNAL_SERVER_ERROR)
        with pytest.raises(ResponseServerError):
            validate_response_status(response)

    def test_client_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.NOT_FOUND)
        with pytest.raises(ResponseClientError):
            validate_response_status(response)

    def test_expected_404_no_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.NOT_FOUND)
        validate_response_status(response, expected_status_code=HTTPStatus.NOT_FOUND)

    def test_redirect_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.MOVED_PERMANENTLY)
        with pytest.raises(ResponseRedirectError):
            validate_response_status(response)

    def test_redirect_no_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.MOVED_PERMANENTLY)
        validate_response_status(response, allow_redirects=True)

    def test_ok_no_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.OK)
        validate_response_status(response)

    def test_unexpected_ok_error_response(self):
        response = MockResponse(self.JSON_BODY, HTTPStatus.OK)
        with pytest.raises(UnexpectedValueError):
            validate_response_status(response, expected_status_code=HTTPStatus.CREATED)

    def test_server_error(self):
        code = HTTPStatus.INTERNAL_SERVER_ERROR
        with pytest.raises(ResponseServerError):
            validate_response_status(code)

    def test_client_error(self):
        code = HTTPStatus.NOT_FOUND
        with pytest.raises(ResponseClientError):
            validate_response_status(code)

    def test_expected_404_no_error(self):
        code = HTTPStatus.NOT_FOUND
        validate_response_status(code, expected_status_code=HTTPStatus.NOT_FOUND)

    def test_redirect_error(self):
        code = HTTPStatus.MOVED_PERMANENTLY
        with pytest.raises(ResponseRedirectError):
            validate_response_status(code)

    def test_redirect_no_error(self):
        code = HTTPStatus.MOVED_PERMANENTLY
        validate_response_status(code, allow_redirects=True)

    def test_ok_no_error(self):
        code = HTTPStatus.OK
        validate_response_status(code)

    def test_unexpected_ok_error(self):
        code = HTTPStatus.OK
        with pytest.raises(UnexpectedValueError):
            validate_response_status(code, expected_status_code=HTTPStatus.CREATED)
