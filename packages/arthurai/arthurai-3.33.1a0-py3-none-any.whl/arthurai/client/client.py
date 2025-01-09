from datetime import timedelta
from typing import Optional, List, Union, Dict, Callable, Tuple
import os
from distutils.util import strtobool
from platform import system
from http import HTTPStatus
from datetime import datetime
import logging
from getpass import getpass

from arthurai.client.auth import AuthRefresher
from arthurai.client.helper import get_current_org
from arthurai.client.http.arthur import FALSE_OFFLINE_DEFAULT
from arthurai.client.http.requests import HTTPClient
from arthurai.common.constants import (
    InputType,
    OutputType,
    TextDelimiter,
    Role,
    DEFAULT_SERVICE_ACCOUNT,
    API_PREFIX,
)
from arthurai.common.exceptions import (
    MissingParameterError,
    UserTypeError,
    UserValueError,
    arthur_excepted,
)
from arthurai.core.models import ArthurModel, ArthurModelGroup
from arthurai.client.validation import validate_response_status
from arthurai.version import __version__ as arthur_version
from arthurai.client.helper import user_login

UNKNOWN_ORG_ID = "unknown"
ORG_ID_BODY = "organization_id"
ORG_ID_HEADER = "Arthur-Organization-ID"

logger = logging.getLogger(__name__)


def new_requests_client(
    access_key: Optional[str] = None,
    url: Optional[str] = None,
    verify_ssl: bool = True,
    offline: bool = False,
    organization_id: Optional[str] = None,
    allow_insecure: bool = False,
    header_refresh_func: Optional[
        Callable[[], Tuple[Dict[str, str], timedelta]]
    ] = None,
) -> HTTPClient:
    if access_key is None:
        access_key = os.getenv("ARTHUR_API_KEY")
    if url is None:
        url = os.getenv("ARTHUR_ENDPOINT_URL")

    if url is None or access_key is None:
        raise MissingParameterError(
            "Please set api key and url either via environment variables "
            "(`ARTHUR_API_KEY` and `ARTHUR_ENDPOINT_URL`) or by passing parameters "
            "`access_key` and `url`."
        )

    if offline and organization_id is not None:
        raise UserValueError(
            "You cannot specify an organization ID if you are offline."
        )

    if organization_id is None:
        organization_id = os.getenv("ARTHUR_ORGANIZATION_ID", None)

    if offline:
        org_id = UNKNOWN_ORG_ID
    elif organization_id is not None:
        org_id = organization_id
    else:
        org_id = get_current_org(url, API_PREFIX, access_key, verify_ssl=verify_ssl)
    user_agent = f"arthur-sdk/{arthur_version} (system={system()})"
    headers = {
        "Accept": "application/json",
        "Authorization": access_key,
        "User-Agent": user_agent,
        ORG_ID_HEADER: org_id,
    }
    return HTTPClient(
        base_url=url,
        path_prefix=API_PREFIX,
        default_headers=headers,
        verify_ssl=verify_ssl,
        allow_insecure=allow_insecure,
        header_refresh_func=header_refresh_func,
    )


class ArthurAI(object):
    """A client that interacts with Arthur's servers."""

    def __init__(
        self,
        config=None,
        verify_ssl=None,
        url=None,
        access_key=None,
        offline=FALSE_OFFLINE_DEFAULT,
        login: str = None,
        password: str = None,
        organization_id: Optional[str] = None,
        allow_insecure: bool = False,
    ):
        verify_ssl_env_var = os.getenv("VERIFY_SSL")
        if verify_ssl is not None:
            if not isinstance(verify_ssl, bool):
                raise UserTypeError("verify_ssl must be of type bool")
            self.verify_ssl = verify_ssl
        elif verify_ssl_env_var:
            try:
                self.verify_ssl = bool(strtobool(verify_ssl_env_var))
            except ValueError:
                raise UserValueError(
                    "Environment Variable VERIFY_SSL must be one of True, true, T, t, False, false, F, f, 1, 0"
                )
        else:
            self.verify_ssl = True

        # "config" dict with params for backwards compatibility
        if config:
            self.client = new_requests_client(verify_ssl=self.verify_ssl, **config)
            return

        # populate login/password from environment if supplied and access_key is not supplied
        if access_key is None:
            login_env = os.getenv("ARTHUR_LOGIN")
            if login is None and login_env is not None:
                login = login_env
            password_env = os.getenv("ARTHUR_PASSWORD")
            if password is None and password_env is not None:
                password = password_env

        if login is not None:
            # if password not supplied, get it from input
            if password is None:
                password = getpass(f"Please enter password for {login}: ")

            # Get session token from login and password
            auth_token, _ = user_login(
                api_http_host=url,
                api_prefix=API_PREFIX,
                login=login,
                password=password,
                verify_ssl=self.verify_ssl,
            )
            # create an auth refresher
            auth_refresher = AuthRefresher(
                url=url, login=login, password=password, verify_ssl=verify_ssl
            )
            # create the client
            self.client = new_requests_client(
                access_key=auth_token,
                url=url,
                verify_ssl=self.verify_ssl,
                offline=offline,
                organization_id=organization_id,
                allow_insecure=allow_insecure,
                header_refresh_func=auth_refresher.refresh,
            )
        else:
            self.client = new_requests_client(
                access_key=access_key,
                url=url,
                verify_ssl=self.verify_ssl,
                offline=offline,
                organization_id=organization_id,
                allow_insecure=allow_insecure,
            )

    def model(
        self,
        partner_model_id: Optional[str] = None,
        input_type: Optional[InputType] = None,
        output_type: Optional[OutputType] = None,
        model_type: Optional[OutputType] = None,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        classifier_threshold: Optional[float] = None,
        is_batch: bool = False,
        text_delimiter: Optional[TextDelimiter] = None,
        expected_throughput_gb_per_day: Optional[int] = None,
        pixel_height: Optional[int] = None,
        pixel_width: Optional[int] = None,
    ) -> ArthurModel:
        """Create a new multistage model.

        :param partner_model_id: The string external id of the model. If display_name is provided without partner_model_id,
            we will generate a unique partner_model_id.
        :param input_type: the :py:class:`.InputType`
        :param output_type: the :py:class:`.OutputType`
        :param model_type: .. deprecated:: version 2.0.0 Use `output_type` instead.
        :param display_name: Optional name to display on dashboard, will default to the external id
        :param description: Optional description for the model
        :param tags: A list of string tags to associate with the model
        :param classifier_threshold: For binary classification models this is the threshold to determine a positive class, defaults to 0.5
        :param is_batch: boolean value which signifies whether the model sends inferences by batch or streaming
        :param text_delimiter: TextDelimiter used in NLP models to split documents into tokens for explanations
        :param expected_throughput_gb_per_day: Expected amount of throughput. Used to provision resources
        :param pixel_height: Image height in pixels. Needed for CV models which require images to be one size
        :param pixel_width: Image width in pixels. Needed for CV models which require images to be one size

        :return: An :py:class:`~arthurai.client.apiv3.model.ArthurModel`
        """
        if input_type is None:
            # marked as an optional parameter in the signature to maintain order of parameters
            raise MissingParameterError("input_type must be specified.")

        if output_type is None and model_type is None:
            raise MissingParameterError(
                "Either 'output_type' or 'model_type' parameter must be specified"
            )
        output_type = output_type if output_type is not None else model_type

        if partner_model_id is None and display_name is None:
            raise MissingParameterError(
                "Either 'partner_model_id' or 'display_name' parameter must be specified"
            )
        elif partner_model_id is None and display_name is not None:
            partner_model_id = (
                display_name.replace(" ", "_")
                + "_"
                + datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            )
        elif display_name is None:
            display_name = partner_model_id

        return ArthurModel(
            client=self.client,
            partner_model_id=partner_model_id,
            input_type=input_type,
            output_type=output_type,
            display_name=display_name,
            description=description,
            tags=tags,
            classifier_threshold=classifier_threshold,
            is_batch=is_batch,
            text_delimiter=text_delimiter,
            expected_throughput_gb_per_day=expected_throughput_gb_per_day,
            pixel_height=pixel_height,
            pixel_width=pixel_width,
        )

    @arthur_excepted("failed to retrieve model")
    def get_model(self, identifier: str, id_type: str = "id") -> ArthurModel:
        """Retrieve an existing model by id

        :param: identifier: Id to get the model by
        :param: id_type: Type of id the identifier is, possible options are ['id', 'partner_model_id']
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: model read
        """
        if id_type in ["partner_model_id", "id"]:
            endpoint = f"/models/{identifier}?id_type={id_type}&expand=attributes"
        else:
            raise UserValueError(
                f"Invalid id_type: {id_type}, must be one of the following ['id', 'partner_model_id]"
            )

        resp = self.client.get(
            endpoint, return_raw_response=True, validation_response_code=HTTPStatus.OK
        )

        # accuracy data is only used by the UI not needed in the SDK
        model_data = resp.json()
        if "accuracy_enabled" in model_data:
            del model_data["accuracy_enabled"]

        model = ArthurModel.from_dict(model_data)
        model._update_client(self.client)
        return model

    @arthur_excepted("failed to retrieve model group")
    def get_model_group(self, id_or_model: Union[str, ArthurModel]) -> ArthurModelGroup:
        """(BETA) Retrieve an existing model group by id

        :param: identifier: Id to get the model group by
        :raises ArthurUserError: failed due to user error
        :raises ArthurUnexpectedError: failed due to an unexpected error
        :permissions: model_group read
        """
        if isinstance(id_or_model, str):
            return ArthurModelGroup._get_model_group(id_or_model, self.client)
        elif isinstance(id_or_model, ArthurModel):
            if id_or_model.model_group_id is not None:
                return ArthurModelGroup._get_model_group(
                    id_or_model.model_group_id, self.client
                )
            else:
                raise UserValueError(
                    "ArthurModel provided has no assigned model_group_id."
                )
        else:
            raise UserTypeError("Provided neither a string ID or ArthurModel instance.")

    @arthur_excepted("failed to get service accounts")
    def get_service_accounts(self, description: Optional[str] = None):
        """Retrieve service accounts

        :param description: an optional description that returned account should match
        :return: parsed response containing a list of service accounts, in the following format:

            .. code-block:: python

                [
                    {
                        "id": "<service account id>",
                        "organization_id": "<organization id>",
                        "description": "<service account description>",
                        "token": "<service account api key>"
                    }
                ]

        """
        endpoint = "/service_accounts"
        params = None if description is None else {"description": description}
        resp = self.client.get(
            endpoint=endpoint, params=params, return_raw_response=True
        )
        validate_response_status(resp, expected_status_code=HTTPStatus.OK)

        return resp.json()["data"]

    @arthur_excepted("failed to create service account")
    def create_service_account(self, description: str, role: Role):
        """Create a new service account

        :param description: the description for the new service account
        :param role: the Role of the new service account
        :return: parsed response in the following format:

            .. code-block:: python

                {
                    "id": "<service account id>",
                    "organization_id": "<organization id>",
                    "description": "<service account description>",
                    "token": "<service account api key>"
                }
        """
        endpoint = "/service_accounts"
        body = {"description": description, "role": role}
        resp = self.client.post(endpoint=endpoint, json=body, return_raw_response=True)
        validate_response_status(resp, expected_status_code=HTTPStatus.CREATED)

        return resp.json()

    @arthur_excepted("failed to retrieve current organization")
    def get_current_org(self) -> Dict[str, str]:
        """Retrieves the current organization that the client is operating in

        :return: a string with the UUID of the current organization
        :permissions: N/A
        """
        endpoint = "/organizations/current"
        response = self.client.get(endpoint, return_raw_response=True)
        validate_response_status(response, expected_status_code=HTTPStatus.OK)
        return response.json()

    @arthur_excepted("failed to set the current organization")
    def set_current_org(self, org_id: str) -> None:
        """Sets the current organization that the client's requests apply to

        :param org_id: The ID of the organization to set
        :return: None
        :permissions: N/A
        """
        # Set the current_org with a PUT request which returns a cookie which gets saved on the HTTPClient session
        endpoint = "/organizations/current"
        body = {"organization_id": org_id}
        response = self.client.put(endpoint, json=body, return_raw_response=True)
        validate_response_status(response, expected_status_code=HTTPStatus.OK)

        # Update the client headers to use the correct org_id for consistency and debugging
        user_agent = f"arthur-sdk/{arthur_version} (system={system()})"
        updated_headers = {"User-Agent": user_agent, ORG_ID_HEADER: org_id}
        self.client.session.headers.update(updated_headers)
