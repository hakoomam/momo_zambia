
frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        if (frm.doc.docstatus === 1 && frm.doc.outstanding_amount > 0) {
            frm.add_custom_button("Pay via MoMo", () => {
                frappe.prompt([
                    {
                        fieldname: "mobile",
                        fieldtype: "Data",
                        label: "MTN Mobile Number (e.g. 260970xxxxxx)",
                        reqd: 1
                    }
                ],
                (values) => {
                    frappe.call({
                        method: "momo_zambia.momo_zambia.api.payment.initiate_payment",
                        args: {
                            mobile: values.mobile,
                            amount: frm.doc.outstanding_amount,
                            currency: frm.doc.currency,
                            external_id: frm.doc.name
                        },
                        callback(r) {
                            if (!r.exc) {
                                frappe.msgprint("MoMo payment initiated. Ref ID: " + r.message.reference_id);
                            }
                        }
                    });
                });
            });
        }
    }
});
