
import frappe
import uuid
from momo_zambia.utils.auth import get_momo_token
import requests

@frappe.whitelist(allow_guest=True)
def initiate_payment(mobile, amount, currency="ZMW", external_id=None):
    settings = frappe.get_single("MoMo Settings")
    if not external_id:
        external_id = str(uuid.uuid4())

    token = get_momo_token(
        subscription_key=settings.subscription_key,
        api_user=settings.api_user,
        api_key=settings.api_key,
        target_environment=settings.target_environment
    )

    reference_id = str(uuid.uuid4())
    url = "https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay" if settings.target_environment == "sandbox"         else "https://proxy.momoapi.mtn.com/collection/v1_0/requesttopay"

    headers = {
        "Authorization": f"Bearer {token}",
        "X-Reference-Id": reference_id,
        "X-Target-Environment": settings.target_environment,
        "Ocp-Apim-Subscription-Key": settings.subscription_key,
        "Content-Type": "application/json"
    }

    data = {
        "amount": str(amount),
        "currency": currency,
        "externalId": external_id,
        "payer": {"partyIdType": "MSISDN", "partyId": mobile},
        "payerMessage": "Payment via ERPNext",
        "payeeNote": "MoMo Zambia"
    }

    try:
        frappe.logger("momo").info(f"Initiating payment request for {mobile}, amount: {amount}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        frappe.logger("momo").info(f"Payment request initiated successfully, reference_id: {reference_id}")
        return {"status": "initiated", "reference_id": reference_id}
    except requests.exceptions.HTTPError as http_err:
        frappe.logger("momo").error(f"HTTP error during payment initiation: {http_err.response.text}")
        frappe.throw(f"Payment initiation failed: {http_err.response.text}")
    except Exception as err:
        frappe.logger("momo").error(f"Unexpected error during payment initiation: {str(err)}")
        frappe.throw(f"Unexpected error: {str(err)}")
        