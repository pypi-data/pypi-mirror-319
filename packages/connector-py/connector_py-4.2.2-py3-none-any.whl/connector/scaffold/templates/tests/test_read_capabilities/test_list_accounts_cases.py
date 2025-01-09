"""Cases for testing ``list_accounts`` capability."""

import typing as t

import httpx
from connector.generated import (
    Error,
    ErrorCode,
    ErrorResponse,
    ListAccounts,
    ListAccountsRequest,
    ListAccountsResponse,
    Page,
)
from connector.generated.models.standard_capability_name import StandardCapabilityName

from tests.common_mock_data import INVALID_AUTH, SETTINGS, VALID_AUTH
from connector.tests.type_definitions import MockedResponse, ResponseBodyMap

Case: t.TypeAlias = tuple[
    StandardCapabilityName,
    ListAccountsRequest,
    ResponseBodyMap,
    ListAccountsResponse | ErrorResponse,
]


def case_list_accounts_200() -> Case:
    """Successful request."""
    args = ListAccountsRequest(
        request=ListAccounts(),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListAccountsResponse(
        response=[],
        page=Page(
            token="9182a8656e64706f696e74a62f7573657273a66f666673657400",
            size=5,
        ),
    )
    return StandardCapabilityName.LIST_ACCOUNTS, args, response_body_map, expected_response


def case_list_accounts_200_no_accounts() -> Case:
    """No accounts found."""
    args = ListAccountsRequest(
        request=ListAccounts(),
        auth=VALID_AUTH,
        settings=SETTINGS,
    )
    response_body_map = {{
        "GET": {{
            "/users?limit=5&offset=0": MockedResponse(
                status_code=httpx.codes.OK,
                response_body={{}},
            ),
        }},
    }}
    expected_response = ListAccountsResponse(
        response=[],
        page=Page(
            token="9182a8656e64706f696e74a62f7573657273a66f666673657400",
            size=5,
        ),
    )
    return StandardCapabilityName.LIST_ACCOUNTS, args, response_body_map, expected_response
