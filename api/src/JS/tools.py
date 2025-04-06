import datetime
import pytz
import hmac
import hashlib
from JS.config import (
    CLIENT_API_KEY,
    CLIENT_SECRET_KEY,
    BASE_URL,
    API_VERSION,
    SIGNATURE_VERSION,
    SIGNATURE_METHOD,
    FORMAT,
)


def get_current_date():
    """
    Gets the current date in the required format.
    Returns:
        str: The current date in YYMMDDHHmmssZZ format.
    """
    # Format current time to match 'YYMMDDHHmmssZZ'
    now = datetime.datetime.now(pytz.UTC)
    # print("Current UTC time:", now.strftime('%y%m%d%H%M%S%z'))
    return now.strftime("%y%m%d%H%M%S%z")


def calculate_signature(to_sign, secret_key):
    """
    Calculates the signature for the given data and secret key.
    Args:
        to_sign (str): The data to sign.
        secret_key (str): The secret key.
    Returns:
        str: The calculated signature.
    """
    # Create an HMAC-SHA256 hash
    signature = hmac.new(
        secret_key.encode("utf-8"), to_sign.encode("utf-8"), hashlib.sha256
    ).digest()

    # Convert to base64 and replace characters
    import base64

    b64_signature = base64.b64encode(signature).decode("utf-8")
    return b64_signature.replace("/", "_").replace("+", "-").replace("=", "")


def build_public_request_url(action, date):
    """
    Builds the public request URL for actions that don't require user authentication.
    Args:
        action (str): The API action.
        date (str): The date string.
    Returns:
        str: The constructed public request URL.
    """
    data_to_sign = f"{action}/{CLIENT_API_KEY}/{API_VERSION}/{SIGNATURE_VERSION}/{SIGNATURE_METHOD}/{date}/{FORMAT}"
    signature = calculate_signature(data_to_sign, CLIENT_SECRET_KEY)
    return f"{BASE_URL}/{action}/{CLIENT_API_KEY}/{API_VERSION}/{SIGNATURE_VERSION}/{SIGNATURE_METHOD}/{signature}/{date}/{FORMAT}"


def build_request_url(action, username, user_secret_key, auth_type, date):
    """
    Builds the request URL for actions that require user authentication.
    Args:
        action (str): The API action.
        username (str): The username.
        user_secret_key (str): The user's secret key.
        auth_type (str): The authentication type.
        date (str): The date string.
    Returns:
        str: The constructed request URL.
    """
    auth_query = f"?authType={auth_type}" if auth_type else ""
    data_to_sign = f"{action}/{CLIENT_API_KEY}/{username}/{API_VERSION}/{SIGNATURE_VERSION}/{SIGNATURE_METHOD}/{date}/{FORMAT}"
    signature = calculate_signature(data_to_sign, CLIENT_SECRET_KEY + user_secret_key)
    return f"{BASE_URL}/{action}/{CLIENT_API_KEY}/{username}/{API_VERSION}/{SIGNATURE_VERSION}/{SIGNATURE_METHOD}/{signature}/{date}/{FORMAT}{auth_query}"

def get_secure_url(username, user_secret_key, action, auth_type, date):
    """
    Constructs a secure URL for the given user, action, and authentication type.
    Args:
        username (str): The username.
        user_secret_key (str): The user's secret key.
        action (str): The API action.
        auth_type (str): The authentication type.
        date (str): The date string.
    Returns:
        str: The secure URL.
    """
    url = build_request_url(action, username, user_secret_key, auth_type, date)
    print("🔗 Secure URL:", url)
    return url