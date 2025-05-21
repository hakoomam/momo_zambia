# hooks.py

override_whitelisted_methods = {
    "momo_zambia.momo_zambia.api.payment.initiate_payment": "momo_zambia.momo_zambia.api.payment.initiate_payment"
}

has_web_view = True


app_name = "momo_zambia"
app_title = "MoMo Zambia"
app_publisher = "Your Name"
app_version = "0.0.1"

# Add webhooks and API whitelisted routes
doc_events = {
    "*": {
        "on_update": "momo_zambia.momo_zambia.api.webhook.momo_callback"
    }
}


override_whitelisted_methods.update({
    "momo_zambia.momo_zambia.api.status.check_status": "momo_zambia.momo_zambia.api.status.check_status",
    "momo_zambia.momo_zambia.api.webhook.momo_callback": "momo_zambia.momo_zambia.api.webhook.momo_callback"
})

doctype_js = {
    "Sales Invoice": "public/js/sales_invoice.js"
}

scheduler_events = {
    "cron": {
        "0/30 * * * *": [
            "momo_zambia.momo_zambia.retry.retry_failed_disbursements"
        ]
    }
}
