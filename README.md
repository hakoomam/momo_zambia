
# MoMo Zambia ERPNext Integration

This app provides full integration of MTN Mobile Money (MoMo) services into ERPNext for Zambia. It includes both **Collections (receiving money)** and **Disbursements (sending money)**, along with a dashboard, retry automation, customer portals, SMS alerts, and QR code generation.

---

## 📦🔧 Features:

    📲 Receive Payments via MTN MoMo STK Push (Customer-Initiated)

    📤 Send Disbursements to MTN mobile numbers (Payouts to suppliers or staff)

    🧾 Sales Invoice Integration with "Pay via MoMo" button

    🔁 Webhook Listener for automatic payment confirmation and Payment Entry creation

    🔁 Retry Scheduler for failed disbursements (every 30 minutes)

    📈 Dashboard Chart summarizing MoMo transaction status

    🧾 QR Code Generator for invoice payment via scan

    📧 SMS Notification Utility ready for Africa’s Talking or MTN APIs

    🔐 Customer Portals (public and login-secured) to check transaction history

    🧪 Sandbox Setup with test data loader and mock customer transactions

    ✅ MIT Licensed, fully open-source, and developer friendly

---

## 🛠 Installation
✅ Requirements

    ERPNext v15+

    Active MTN Developer Account (MoMo Collection and/or Disbursement keys)

    Valid API credentials and callback whitelisting

### 1. Install the app
```bash
bench get-app momo_zambia https://github.com/hakoomam/momo_zambia
bench --site yoursite install-app momo_zambia
bench --site yoursite migrate
```

### 2. Setup Mode of Payment
- Add `MTN MoMo` to **Mode of Payment**
- Link it to a **Mode of Payment Account** (Bank or Cash account)

---

## ⚙️ Configuration

### MoMo Settings
Navigate to `MoMo Settings` in ERPNext and configure:
- Subscription Key
- API User
- API Key
- Target Environment (sandbox or production)
- Callback URL:  
  `https://yourdomain/api/method/momo_zambia.momo_zambia.api.webhook.momo_callback`

🧪 Testing (with sandbox data)
bench --site yoursite execute momo_zambia.momo_zambia.sandbox.load_test_data
---

## 💰 Payment via Sales Invoice

1. Submit a Sales Invoice.
2. Click **"Pay via MoMo"** button.
3. Enter mobile number.
4. Customer receives STK push.
5. Upon success, a Payment Entry is automatically created.

---

## 📤 Disbursements

Use API:
```
/api/method/momo_zambia.momo_zambia.api.disbursement.send_money
```
Payload:
```json
{
  "mobile": "26097XXXXXX",
  "amount": 150,
  "external_id": "PAYOUT-001"
}
```

---

## 🔄 Auto-Retry Scheduler

A background job runs every 30 minutes:
- Retries disbursements with status `FAILED` or `PENDING`.

---

## 🔐 Portals

### Public:
- `/assets/momo_zambia/portal.html`

### Login Protected:
- `/assets/momo_zambia/secure_portal.html`
- Use ERPNext User credentials (email/password)

---

## 📲 SMS Notifications

Use:
```python
frappe.call("momo_zambia.momo_zambia.sms_utils.send_sms", {
    "mobile": "26097XXXXXX",
    "message": "Your payment was successful."
})
```

To integrate with:
- **Africa's Talking**:
  - API URL: `https://api.africastalking.com/version1/messaging`
  - Header: `apiKey`, `username`
  - POST body: `to`, `message`

- **MTN SMS Gateway**: contact MTN Zambia for credentials.

---

## 🧾 QR Codes

To embed a payment QR in the Sales Invoice print format:
```html
<img src="{{ frappe.call('momo_zambia.momo_zambia.qr_utils.get_invoice_qr', invoice_name=doc.name) }}" width="180" />
```

---

## 📈 Dashboard Chart

- Chart: `MoMo Transactions Summary`
- Type: Group By (status)
- Source: `Disbursement Log`

---

## 📧 Email Alerts

Extend `alerts.py` to send internal alerts on events.

---

## 🙋 Support

For custom enhancements, integrations, or questions, contact:
**Developer:** Miyanda Hakooma  
**Email:** mh@antares.co.zm  
**Github:** @hakoomam

---

## ⚠️ Disclaimer

This software is provided “as is” with no warranties. The author is not affiliated with MTN Zambia or its subsidiaries. You assume all responsibility for usage, and the author is not liable for any losses, outages, or damages resulting from use of this integration, whether in testing or production environments.
