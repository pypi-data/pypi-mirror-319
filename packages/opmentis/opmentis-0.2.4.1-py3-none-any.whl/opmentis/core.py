import requests
from typing import Dict, Optional, Union
from rich.console import Console
from rich.table import Table
from rich.text import Text

# Base URLs for the API
BASE_URL = "https://api.opmentis.xyz/api/v1"
FOODBOT_URL = "https://labfoodbot.opmentis.xyz/api/v1"


def get_headers(token: str) -> Dict[str, str]:
    """
    Generate headers for authenticated requests.
    """
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def send_request(method: str, url: str, **kwargs) -> Optional[Union[Dict, str]]:
    """
    Send an HTTP request and handle common errors.
    Args:
        method (str): HTTP method (e.g., GET, POST).
        url (str): The API endpoint URL.
        kwargs: Additional arguments for the request (e.g., headers, json).
    Returns:
        Optional[Union[Dict, str]]: Parsed response or None on failure.
    """
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:  # noqa: F841
        # print(f"Request failed. Error: {e.response.status_code if e.response else 'Unknown Error'}")
        return "Request failed"


def get_active_lab() -> Optional[Dict]:
    """
    Fetch the active lab details from the central API endpoint.
    """
    endpoint = f"{BASE_URL}/labs/labs/active"
    return send_request("GET", endpoint)


def authenticate(wallet_address: str) -> Optional[str]:
    """
    Authenticate a user based on their wallet address.
    Returns an authentication token if successful.
    """
    endpoint = f"{BASE_URL}/authenticate"
    params = {"wallet_address": wallet_address}
    response = send_request("POST", endpoint, params=params)
    return response.get("access_token") if response else None


def register_user(
    wallet_address: str, labid: str, role_type: str
) -> Dict[str, Union[str, Dict]]:
    """
    Register a user as a miner or validator and add a stake for them.
    """
    # Authenticate the user
    token = authenticate(wallet_address)
    if not token:
        return {"error": "Authentication failed. Could not obtain access token."}

    # Prepare headers with the token
    headers = get_headers(token)

    # Define endpoints for registration and adding stake
    register_endpoint = f"{BASE_URL}/labs/labs/{labid}/{role_type}/register"

    # Prepare payload for registration
    register_payload = {"wallet_address": wallet_address}
    registration_response = send_request(
        "POST", register_endpoint, json=register_payload, headers=headers
    )
    if not registration_response:
        return {"error": f"Failed to register as {role_type}."}

    # Parse the registration response
    try:
        # Extract details from the correct keys in the response
        message = registration_response.get("message", {})
        status = message.get("status", "failure")
        external_response = message.get("external_response", {})  # noqa: F841
        internal_data = message.get("internal_data", "")  # noqa: F841
        user_message = message.get("message", "")

        if status == "success":
            return {
                "status": "success",
                "message": user_message,
            }
        else:
            return {
                "status": "failure",
                "message": user_message or "Unknown error occurred.",
            }
    except Exception as e:  # noqa: F841
        return {"error": "An error occurred while parsing the registration response."}


def fetch_user_data(endpoint: str, wallet_address: str) -> Union[Dict, str]:
    """
    Fetch user data or points from a specified endpoint.
    """
    token = authenticate(wallet_address)
    if not token:
        return {"error": "Authentication required to fetch user data."}

    headers = get_headers(token)
    payload = {"wallet_address": wallet_address}
    response = send_request("POST", endpoint, json=payload, headers=headers)
    return response if response else {"error": "Failed to fetch user data."}


def render_table(
    wallet_address: str, data: Union[Dict, str], title: str = "User Data"
) -> str:
    """
    Render user data as a formatted and colorful table with a dynamic title.
    Args:
        wallet_address (str): The wallet address of the user.
        data (Union[Dict, str]): The user data to be formatted.
        title (str): The title of the table (default is "User Data").
    Returns:
        str: A colorful table as a string for terminal output.
    """
    console = Console()

    if isinstance(data, dict):
        # Create a rich table with a dynamic title
        table = Table(title=title, title_style="cyan")

        # Add columns
        table.add_column(wallet_address, style="dodger_blue3", justify="left")
        table.add_column("Value", style="bold white", justify="right")

        # Add rows from the data dictionary
        for key, value in data.items():
            table.add_row(
                Text(key, style="dodger_blue3"), Text(str(value), style="white")
            )

        # Print the table
        console.print(table)
        return "Table rendered in the console."

    elif isinstance(data, str):
        # If the data is already a string, just print it
        console.print(Text(data, style="white"))
        return data

    return "Invalid data format. Unable to render table."


def userdata(labid: str, wallet_address: str) -> Union[str, Dict]:
    """
    Fetch user data and return it as a formatted table or raw string.
    Args:
        labid (str): The lab ID to validate registration.
        wallet_address (str): The wallet address of the user.
    Returns:
        Union[str, Dict]: A formatted table as a string or an error message.
    """
    # Validate user registration and requirements
    validation_error = validate_user_registration(labid, wallet_address)
    if validation_error:
        return validation_error

    endpoint = f"{FOODBOT_URL}/user_data/table"
    payload = {"wallet_address": wallet_address}
    token = authenticate(wallet_address)

    if not token:
        return "Authentication required to fetch user data."

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()

        user_table = response.json().get("user_table", "")
        return render_table(
            wallet_address, user_table, title="User Balance Information"
        )

    except requests.exceptions.RequestException as e:  # noqa: F841
        # print(f"Failed to fetch user data. Error")
        return "Failed to fetch user data."


def userpoint(labid: str, wallet_address: str) -> str:
    """
    Fetch user points from the API and return as a formatted table.
    Args:
        labid (str): The lab ID to validate registration.
        wallet_address (str): The user's wallet address.
    Returns:
        str: Formatted table or error message.
    """
    # Validate user registration and requirements
    validation_error = validate_user_registration(labid, wallet_address)
    if validation_error:
        return validation_error

    endpoint = f"{BASE_URL}/labs/get-user-point"
    payload = {"labid": labid, "wallet_address": wallet_address}
    token = authenticate(wallet_address)

    if not token:
        return "Authentication required to fetch user points."

    headers = get_headers(token)
    response = send_request("POST", endpoint, json=payload, headers=headers)
    if response:
        user_table = response.get("user_data", {})
        return render_table(wallet_address, user_table, title="User Point Information")
    return "Failed to fetch user points."


def check_user_balance(labid: str, wallet_address: str) -> Union[str, Dict]:
    """
    Fetch user balance from the API and return it as a formatted table or raw string.
    Args:
        labid (str): The lab ID to validate registration.
        wallet_address (str): The wallet address of the user.
    Returns:
        Union[str, Dict]: A formatted table as a string or an error message.
    """
    # Validate user registration and requirements
    validation_error = validate_user_registration(labid, wallet_address)
    if validation_error:
        return validation_error

    endpoint = f"{BASE_URL}/labs/user/balance/{wallet_address}/{labid}"
    token = authenticate(wallet_address)

    if not token:
        return "Authentication required to check user balance."

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()

        # Parse the response
        response_data = response.json()
        if response_data.get("status") == "success":
            data = response_data.get("data", {})
            incentive_balance = data.get("incentive_balance", 0)
            bonus_balance = data.get("bonus_balance", 0)
            total_balance = incentive_balance + bonus_balance

            # Format balances with commas
            formatted_incentive = f"{incentive_balance:,.2f}"
            formatted_bonus = f"{bonus_balance:,.2f}"
            formatted_total = f"{total_balance:,.2f}"

            user_table = {
                "Wallet Address": data.get("wallet_address", "Unknown"),
                "Lab ID": data.get("lab_id", "Unknown"),
                "Incentive Balance": formatted_incentive,
                "Bonus Balance": formatted_bonus,
                "Available Balance": formatted_total,
            }
            return render_table(
                wallet_address, user_table, title="User Balance Information"
            )

        return "Unable to retrieve user balance at this time."

    except requests.exceptions.RequestException:
        # Log the error internally for debugging (without exposing the URL)
        # print("An error occurred while fetching user balance.", exc_info=True)
        return "Unable to retrieve user balance due to an unexpected error."


def request_reward_payment(labid: str, wallet_address: str, request_amount: int) -> str:
    """
    Submit a reward request for the user.
    Args:
        labid (str): The lab ID to submit the reward request.
        wallet_address (str): The user's wallet address.
        request_amount (int): The amount to request as a reward.
    Returns:
        str: Success or error message.
    """
    # Validate user registration and requirements
    validation_error = validate_user_registration(labid, wallet_address)
    if validation_error:
        return validation_error

    endpoint = f"{BASE_URL}/labs/submit_reward_request"
    payload = {
        "lab_id": labid,
        "wallet_address": wallet_address,
        "requested_amount": request_amount,
    }
    token = authenticate(wallet_address)

    if not token:
        return "Authentication required to submit a reward request."

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()

        response_data = response.json()
        if "error" in response_data:
            return response_data["error"]
        status_message = response_data.get("message", "Unknown")
        return f"Reward request status for wallet {wallet_address} in lab {labid}: {status_message}"

    except requests.exceptions.RequestException:
        return "Unable to submit reward request due to an unexpected error."


def show_active_labs(wallet_address: str) -> Union[str, Dict]:
    """
    Fetch and display all active labs associated with a given wallet address.
    Args:
        wallet_address (str): The wallet address of the user.
    Returns:
        Union[str, Dict]: A formatted table as a string or an error message.
    """
    endpoint = f"{BASE_URL}/labs/labs/active/{wallet_address}"
    token = authenticate(wallet_address)

    if not token:
        return "Authentication required to fetch active labs."

    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()

        # Parse response JSON
        response_data = response.json()
        if response_data.get("status") == "success":
            active_labs = response_data.get("data", [])
            if not active_labs:
                return "No active labs found for the given wallet address."

            # Prepare the data for rendering
            lab_table = {
                lab.get("labid", "Unknown"): lab.get("labname", "Unknown")
                for lab in active_labs
            }
            return render_table(wallet_address, lab_table, title="Active Labs")

        return "Failed to fetch active labs."

    except requests.exceptions.RequestException as e:
        # Return the exception message for better debugging
        return f"Unable to fetch active labs due to an unexpected error: {str(e)}"


def endchat() -> Union[str, Dict]:
    """
    End the chat session and trigger evaluation.
    """
    endpoint = f"{FOODBOT_URL}/end_chat"
    response = send_request("POST", endpoint)
    return (
        response.get("message", "Chat ended and evaluation triggered.")
        if response
        else {"error": "Failed to end chat."}
    )


def validate_user_registration(labid: str, wallet_address: str) -> Optional[str]:
    """
    Validate if a user is registered and meets the requirements for the specified lab.
    Args:
        labid (str): The lab ID to query.
        wallet_address (str): The wallet address of the user.
    Returns:
        Optional[str]: An error message if validation fails, otherwise None.
    """
    user_status = check_user_status(labid, wallet_address)

    # Check if user_status is an error message (string)
    if isinstance(user_status, str):
        return "Failed to fetch user status. Please ensure you are authenticated and registered."

    # If user_status contains an error key, return the error message
    if "error" in user_status:
        return user_status["error"]

    # Check if the user meets the miner or validator requirements
    if not user_status.get("meets_miner_requirements", False) and not user_status.get(
        "meets_validator_requirements", False
    ):
        return "You do not meet the requirements to access this lab. Please ensure you are registered and meet the minimum stake or balance requirements."

    return None  # Validation passed


def check_user_status(labid: str, wallet_address: str) -> Union[Dict, str]:
    """
    Check the user's stake status for a specific lab.
    Args:
        labid (str): The lab ID to query.
        wallet_address (str): The wallet address of the user.
    Returns:
        dict: Response from the API with user stake status.
    """
    # Authenticate the user to obtain a token
    token = authenticate(wallet_address)
    if not token:
        return {"error": "Authentication failed. Could not obtain access token."}

    # Construct the endpoint URL
    endpoint = f"{BASE_URL}/labs/labs/{labid}/wallets/{wallet_address}/status"

    # Set headers for the GET request
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}

    # Make the GET request to fetch the user status
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()  # Raises an error for HTTP codes 4xx/5xx
        user_status = response.json()
        return user_status
    except requests.exceptions.RequestException as e:  # noqa: F841
        return {"error": "Failed to fetch user status."}
