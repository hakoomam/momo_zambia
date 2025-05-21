
import frappe
from frappe.utils import nowdate

@frappe.whitelist(allow_guest=True)
def momo_callback():
    data = frappe.request.get_json()
    frappe.logger("momo").info(f"Received MoMo callback: {data}")

    reference_id = data.get("reference_id")
    if not reference_id:
        return {"error": "Missing reference_id"}

    invoice = frappe.get_doc("Sales Invoice", reference_id)
    if invoice and invoice.outstanding_amount > 0:
        pe = frappe.get_doc({
            "doctype": "Payment Entry",
            "payment_type": "Receive",
            "party_type": "Customer",
            "party": invoice.customer,
            "posting_date": nowdate(),
            "paid_amount": invoice.outstanding_amount,
            "received_amount": invoice.outstanding_amount,
            "received_amount_in_words": "",
            "reference_no": reference_id,
            "reference_date": nowdate(),
            "company": invoice.company,
            "mode_of_payment": "MTN MoMo",
            "paid_to": frappe.get_cached_value("Mode of Payment Account", {"parent": "MTN MoMo"}, "default_account"),
            "references": [
                {
                    "reference_doctype": "Sales Invoice",
                    "reference_name": invoice.name,
                    "allocated_amount": invoice.outstanding_amount
                }
            ]
        })
        pe.insert(ignore_permissions=True)
        pe.submit()
        frappe.logger("momo").info(f"Payment Entry created for {reference_id}")

    return {"status": "Payment Entry created"}
