
import frappe

@frappe.whitelist()
def send_sms(mobile, message):
    # Placeholder for actual integration
    # For Africa's Talking, you'd use requests.post with your API key
    frappe.logger("momo").info(f"Sending SMS to {mobile}: {message}")
    return {"status": "queued", "mobile": mobile}
