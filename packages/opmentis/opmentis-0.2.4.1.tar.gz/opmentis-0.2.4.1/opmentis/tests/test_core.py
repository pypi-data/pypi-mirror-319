import pytest
from unittest.mock import patch
from opmentis import (
    authenticate,
    get_active_lab,
    register_user,
    check_user_status,
    validate_user_registration,
    render_table,
)

BASE_URL = "https://api.opmentis.xyz/api/v1"


# Mock for authenticate
@pytest.fixture
def mock_authenticate():
    return "mocked_token"


# Test authenticate function
@patch("opmentis.core.send_request")
def test_authenticate(mock_send_request):
    mock_send_request.return_value = {"access_token": "mocked_token"}
    token = authenticate("test_wallet")
    assert token == "mocked_token"
    mock_send_request.assert_called_once_with(
        "POST", f"{BASE_URL}/authenticate", params={"wallet_address": "test_wallet"}
    )


# Test get_active_lab function
@patch("opmentis.core.send_request")
def test_get_active_lab(mock_send_request):
    mock_send_request.return_value = {"status": "success", "data": {"lab": "active"}}
    response = get_active_lab()
    assert response == {"status": "success", "data": {"lab": "active"}}
    mock_send_request.assert_called_once_with("GET", f"{BASE_URL}/labs/labs/active")


# Test register_user function
@patch("opmentis.core.authenticate")
@patch("opmentis.core.send_request")
def test_register_user(mock_send_request, mock_authenticate):
    mock_authenticate.return_value = "mocked_token"
    mock_send_request.return_value = {
        "message": {
            "status": "success",
            "message": "Registered successfully",
        }
    }

    response = register_user("test_wallet", "test_labid", "miner")
    assert response == {
        "status": "success",
        "message": "Registered successfully",
    }
    mock_authenticate.assert_called_once_with("test_wallet")
    mock_send_request.assert_called_once_with(
        "POST",
        f"{BASE_URL}/labs/labs/test_labid/miner/register",
        json={"wallet_address": "test_wallet"},
        headers={
            "Authorization": "Bearer mocked_token",
            "Content-Type": "application/json",
        },
    )


# Test check_user_status function
@patch("opmentis.core.authenticate")
@patch("requests.get")
def test_check_user_status(mock_requests_get, mock_authenticate):
    mock_authenticate.return_value = "mocked_token"
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        "status": "success",
        "data": {"valid": True},
    }

    response = check_user_status("test_labid", "test_wallet")
    assert response == {"status": "success", "data": {"valid": True}}
    mock_authenticate.assert_called_once_with("test_wallet")
    mock_requests_get.assert_called_once_with(
        f"{BASE_URL}/labs/labs/test_labid/wallets/test_wallet/status",
        headers={"Authorization": "Bearer mocked_token", "Accept": "application/json"},
    )


# Test validate_user_registration function
@patch("opmentis.core.check_user_status")
def test_validate_user_registration(mock_check_user_status):
    # Simulate valid user status
    mock_check_user_status.return_value = {
        "meets_miner_requirements": True,
        "meets_validator_requirements": False,
    }

    result = validate_user_registration("test_labid", "test_wallet")
    assert result is None  # No error message means validation passed

    # Simulate invalid user status
    mock_check_user_status.return_value = {"meets_miner_requirements": False}
    result = validate_user_registration("test_labid", "test_wallet")
    assert result == (
        "You do not meet the requirements to access this lab. Please ensure you are registered and meet the minimum stake or balance requirements."
    )


# Test render_table function
def test_render_table(capsys):
    data = {"Key1": "Value1", "Key2": "Value2"}
    wallet_address = "test_wallet"

    result = render_table(wallet_address, data, title="Test Table")
    captured = capsys.readouterr()
    assert "Key1" in captured.out
    assert "Value1" in captured.out
    assert "Table rendered in the console." in result
