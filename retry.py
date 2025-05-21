
import frappe
from momo_zambia.momo_zambia.api.disbursement import send_money

def retry_failed_disbursements():
    logs = frappe.get_all("Disbursement Log", filters={"status": ["in", ["FAILED", "PENDING"]]}, fields=["name", "mobile", "amount", "external_id"])
    for log in logs:
        try:
            result = send_money(
                mobile=log.mobile,
                amount=log.amount,
                external_id=log.external_id
            )
            doc = frappe.get_doc("Disbursement Log", log.name)
            doc.status = "RETRIED"
            doc.save(ignore_permissions=True)
            frappe.logger("momo").info(f"Retried disbursement: {log.external_id}")
        except Exception as e:
            frappe.logger("momo").error(f"Retry failed for {log.external_id}: {str(e)}")
