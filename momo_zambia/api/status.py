
import frappe
from momo_zambia.momo_zambia.mtn.collection import Collection

@frappe.whitelist()
def check_status(reference_id):
    settings = frappe.get_single("MoMo Settings")
    momo = Collection(
        subscription_key=settings.subscription_key,
        user_id=settings.api_user,
        api_key=settings.api_key,
        target_environment=settings.target_environment
    )
    momo.get_token()
    status = momo.get_transaction_status(reference_id)
    return status
