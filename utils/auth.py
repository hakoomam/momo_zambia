
import frappe
import requests
from frappe.utils import now_datetime, add_to_date

def get_momo_token(subscription_key, api_user, api_key, target_environment):
    cache_key = f"momo_token_{api_user}"
    token_details = frappe.cache().get_value(cache_key)

    if token_details and token_details["expires_at"] > now_datetime():
        frappe.logger("momo").info("Using cached MoMo token.")
        return token_details["token"]

    url = "https://sandbox.momodeveloper.mtn.com/collection/token/" if target_environment == "sandbox"         else "https://proxy.momoapi.mtn.com/collection/token/"

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Authorization": f"Basic {api_key}",
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        token = response.json()["access_token"]
        frappe.cache().set_value(cache_key, {
            "token": token,
            "expires_at": add_to_date(now_datetime(), minutes=55)
        })
        frappe.logger("momo").info("New MoMo token fetched and cached.")
        return token
    except requests.exceptions.RequestException as e:
        frappe.logger("momo").error(f"Token retrieval error: {str(e)}")
        raise frappe.ValidationError(f"MoMo Token Error: {str(e)}")
        