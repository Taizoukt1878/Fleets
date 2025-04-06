from tools import get_secure_url
from utils import login_user, fetch_cart_items
from config import USERNAME, PASSWORD




def main_flow(id_reporttype=13, id_company=203):
    """
    Main function to orchestrate the login, secure URL generation, and cart item fetching.
    """


    # Step 1: Login
    login_response = login_user(username=USERNAME, password=PASSWORD)
    secret_key = login_response["secretKey"]
    date = login_response["date"]

    if not secret_key:
        print("❌ Failed to retrieve secretKey")
        return

    # Step 2: Build secure URL
    action = 'CartReportByType'
    auth_type = 'user'
    secure_url = get_secure_url(USERNAME, secret_key, action, auth_type, date)
    secure_url_valid = secure_url.replace('auth-service', 'report-service')  # adjust URL to the report-service

    # Step 3: Fetch cart items
    fetch_cart_items(secure_url_valid, id_reporttype, id_company)

if __name__ == "__main__":
    main_flow()