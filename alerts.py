
def send_momo_alert(subject, message):
    recipients = frappe.get_all("User", filters={"enabled": 1, "send_momo_alerts": 1}, pluck="email")
    if recipients:
        frappe.sendmail(
            recipients=recipients,
            subject=subject,
            message=message
        )
