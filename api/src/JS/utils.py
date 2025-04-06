import json
import pprint
import requests
from JS.tools import get_current_date, build_public_request_url

def login_user(username, password):
    """
    Logs in a user and returns their secret key and the date.
    Args:
        username (str): The username.
        password (str): The password.
    Returns:
        dict: The user's secret key and the date.
    """
    date = get_current_date()
    url = build_public_request_url('UserAccountLogin', date)
    response = send(url, {"username": username, "password": password})
    print("🔑 UserAccountLogin response:", response)
    return {"secretKey": response.get("secretKey"), "date": date}

def send(url, body):
    """
    Sends a POST request to the given URL with the provided body.
    Args:
        url (str): The URL to send the request to.
        body (dict): The request body.
    Returns:
        dict: The JSON response from the server.
    """
    response = requests.post(
        url, data=json.dumps(body), headers={"Content-Type": "application/json"}
    )
    return response.json()

def fetch_cart_items(url, id_reporttype, id_company):
    """
    Fetches cart items using the provided URL and body.
    Args:
        url (str): The URL to fetch cart items from.
    Returns:
        dict: The cart items response.
    """
    body = {
        "id_reporttype": id_reporttype,  # Example type: Battery
        "id_company": id_company  # Example Company ID
    }
    response = send(url, body)
    # print("🛒 Cart Items:", response)
    pprint.pprint(f"🛒 Cart Items:{response}", indent=5)
    return response


