
import frappe
import uuid
from momo_zambia.momo_zambia.mtn.collection import Collection

@frappe.whitelist(allow_guest=True)
def initiate_payment(mobile, amount, currency="ZMW", external_id=None):
    settings = frappe.get_single("MoMo Settings")
    if not external_id:
        external_id = str(uuid.uuid4())

    momo = Collection(
        subscription_key=settings.subscription_key,
        user_id=settings.api_user,
        api_key=settings.api_key,
        target_environment=settings.target_environment
    )

    momo.get_token()
    reference_id = str(uuid.uuid4())
    result = momo.request_to_pay(
        reference_id=reference_id,
        mobile=mobile,
        amount=amount,
        currency=currency,
        external_id=external_id,
        payer_message="Payment via ERPNext",
        payee_note="MoMo Zambia"
    )
    return {"status": "initiated", "reference_id": reference_id, "result": result}
