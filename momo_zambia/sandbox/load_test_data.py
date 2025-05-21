
import frappe

def execute():
    # Create demo MoMo Settings
    if not frappe.db.exists("MoMo Settings", None):
        doc = frappe.get_doc({
            "doctype": "MoMo Settings",
            "subscription_key": "test-key",
            "api_user": "test-user",
            "api_key": "test-api-key",
            "target_environment": "sandbox",
            "callback_url": "http://localhost/api/method/momo_zambia.momo_zambia.api.webhook.momo_callback"
        })
        doc.insert()

    # Create dummy customer and Sales Invoice
    if not frappe.db.exists("Customer", "Test Customer"):
        frappe.get_doc({
            "doctype": "Customer",
            "customer_name": "Test Customer",
            "customer_group": "Individual",
            "territory": "Zambia"
        }).insert()

    if not frappe.db.exists("Sales Invoice", "SINV-MOMO"):
        frappe.get_doc({
            "doctype": "Sales Invoice",
            "title": "Test MoMo Invoice",
            "naming_series": "SINV-",
            "customer": "Test Customer",
            "items": [
                {
                    "item_name": "Test Product",
                    "qty": 1,
                    "rate": 150
                }
            ]
        }).insert()
