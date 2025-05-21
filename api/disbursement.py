
import frappe
import uuid
from momo_zambia.momo_zambia.mtn.disbursement import Disbursement

@frappe.whitelist()
def send_money(mobile, amount, currency="ZMW", external_id=None):
    settings = frappe.get_single("MoMo Settings")
    if not external_id:
        external_id = str(uuid.uuid4())

    momo = Disbursement(
        subscription_key=settings.subscription_key,
        user_id=settings.api_user,
        api_key=settings.api_key,
        target_environment=settings.target_environment
    )

    momo.get_token()
    reference_id = str(uuid.uuid4())
    result = momo.transfer(
        reference_id=reference_id,
        mobile=mobile,
        amount=amount,
        currency=currency,
        external_id=external_id,
        payee_note="Sent via ERPNext MoMo",
        payer_message="From ERPNext"
    )
    return {"status": "sent", "reference_id": reference_id, "result": result}
