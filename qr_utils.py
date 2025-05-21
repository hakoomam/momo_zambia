
import frappe
import qrcode
import base64
from io import BytesIO

@frappe.whitelist()
def get_invoice_qr(invoice_name):
    invoice = frappe.get_doc("Sales Invoice", invoice_name)
    mobile = invoice.customer_mobile or "260970000000"  # Assuming mobile is stored on the customer or invoice
    amount = invoice.outstanding_amount
    currency = invoice.currency or "ZMW"
    external_id = invoice.name

    url = f"{frappe.request.host_url}api/method/momo_zambia.momo_zambia.api.payment.initiate_payment?mobile={mobile}&amount={amount}&currency={currency}&external_id={external_id}"

    qr = qrcode.make(url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_base64}"
