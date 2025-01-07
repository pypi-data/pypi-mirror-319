import json

import pytest
import requests
from requests.exceptions import RequestException

from logafault.faults import FaultsAPIError, get_all_faults, log_fault


@pytest.fixture
def mock_get(mocker):
    """Fixture to mock requests.get."""
    return mocker.patch("logafault.faults.requests.get")


@pytest.fixture
def mock_post(mocker):
    """Fixture to mock requests.post."""
    return mocker.patch("logafault.faults.requests.post")


def test_get_all_faults_success(mock_get):
    # Mock a successful response
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1262784,
            "code": "CPWEB1234567",
            "description": "No power in the Gotham area",
            "workType": "No Supply (Area)",
            "status": "Closed_CL",
            "dateCreated": 1530251597000,
            "contactName": "Bruce Wayne",
            "address": "224 Park Drive, Gotham City",
            "latitude": -26.54321,
            "longitude": 27.99999999999999,
        }
    ]

    cookie = "SESSION=mock_session; JSESSIONID=mock_jsessionid"
    faults = get_all_faults(cookie)

    assert len(faults) == 1
    assert faults[0]["code"] == "CPWEB1234567"
    mock_get.assert_called_once_with(
        "https://citypower.mobi/forcelink/za4/rest/calltakemanager/getAllCustomerCalls",
        headers={
            "Content-Type": "application/json",
            "Cookie": cookie,
        },
    )


def test_log_fault_success(mock_post):
    # Mock a successful response for logging a fault
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": "SUCCESS",
        "errorMessage": None,
        "successMessage": None,
        "code": "CPWEB1234567",
        "id": 4689356,
    }

    cookie = "SESSION=mock_session; JSESSIONID=mock_jsessionid"
    fault_data = {
        "workType": "NS",
        "childWorkType": "NSTL",
        "customLookupCode2": "Prepaid",
        "description": ("The traffic light at the intersection is off"),
        "custom2": "1234567890",
        "custom4": "",
        "contactNumber": "0123456789",
        "contactName": "Bruce Wayne",
    }

    response = log_fault(cookie, fault_data)

    assert response["result"] == "SUCCESS"
    assert response["code"] == "CPWEB1234567"
    mock_post.assert_called_once_with(
        "https://citypower.mobi/forcelink/za4/rest/calltakemanager/logCallMyAddress",
        headers={
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://citypower.mobi/logFaultMyAddress",
            "Content-Type": "application/problem+json",
            "Origin": "https://citypower.mobi",
            "Connection": "keep-alive",
            "Cookie": cookie,
        },
        data=json.dumps(fault_data),
    )


def test_log_fault_http_error(mock_post):
    # Mock a response with an HTTP error for logging a fault
    mock_response = mock_post.return_value
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = requests.HTTPError(
        "Internal Server Error"
    )

    cookie = "SESSION=mock_session; JSESSIONID=mock_jsessionid"
    fault_data = {"workType": "NS", "childWorkType": "NSTL"}

    with pytest.raises(FaultsAPIError, match="Failed to log fault:"):
        log_fault(cookie, fault_data)


def test_log_fault_request_exception(mock_post):
    # Simulate a network-related exception when logging a fault
    mock_post.side_effect = RequestException("Network error")

    cookie = "SESSION=mock_session; JSESSIONID=mock_jsessionid"
    fault_data = {"workType": "NS", "childWorkType": "NSTL"}

    with pytest.raises(FaultsAPIError, match="Failed to log fault: Network error"):
        log_fault(cookie, fault_data)


def test_log_fault_invalid_json(mock_post):
    # Mock a response with invalid JSON when logging a fault
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("No JSON object could be decoded")

    cookie = "SESSION=mock_session; JSESSIONID=mock_jsessionid"
    fault_data = {"workType": "NS", "childWorkType": "NSTL"}

    with pytest.raises(
        FaultsAPIError, match="Invalid JSON response: No JSON object could be decoded"
    ):
        log_fault(cookie, fault_data)
