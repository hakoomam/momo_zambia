
import frappe
from frappe import request
from frappe.utils import nowdate

@frappe.whitelist(allow_guest=True)
def momo_callback():
    allowed_ips = ["YOUR_MTN_ALLOWED_IP"]
    if request.remote_addr not in allowed_ips:
        frappe.logger("momo").warning(f"Unauthorized access from IP: {request.remote_addr}")
        frappe.throw("Unauthorized IP address", frappe.PermissionError)

    data = request.get_json()
    frappe.logger("momo").info(f"MoMo webhook received: {data}")

    reference_id = data.get("reference_id")
    if not reference_id:
        frappe.logger("momo").error("Webhook missing reference_id")
        return {"error": "Missing reference_id"}

    try:
        invoice = frappe.get_doc("Sales Invoice", reference_id)
        if invoice.outstanding_amount > 0:
            pe = frappe.get_doc({
                "doctype": "Payment Entry",
                "payment_type": "Receive",
                "party_type": "Customer",
                "party": invoice.customer,
                "posting_date": nowdate(),
                "paid_amount": invoice.outstanding_amount,
                "received_amount": invoice.outstanding_amount,
                "reference_no": reference_id,
                "reference_date": nowdate(),
                "company": invoice.company,
                "mode_of_payment": "MTN MoMo",
                "paid_to": invoice.debit_to
            })
            pe.insert(ignore_permissions=True)
            pe.submit()
            frappe.logger("momo").info(f"Payment Entry created for Invoice: {reference_id}")
            return {"status": "success", "message": "Payment processed"}
    except frappe.DoesNotExistError:
        frappe.logger("momo").error(f"Invoice not found: {reference_id}")
        return {"error": "Invoice not found"}
    except Exception as e:
        frappe.logger("momo").error(f"Error processing webhook: {str(e)}")
        return {"error": f"Processing error: {str(e)}"}
        