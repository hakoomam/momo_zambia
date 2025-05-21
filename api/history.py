
import frappe

@frappe.whitelist(allow_guest=True)
def get_payment_history(mobile):
    return frappe.get_all("Disbursement Log", filters={"mobile": mobile}, fields=["creation", "amount", "status", "reference_id"], order_by="creation desc")
