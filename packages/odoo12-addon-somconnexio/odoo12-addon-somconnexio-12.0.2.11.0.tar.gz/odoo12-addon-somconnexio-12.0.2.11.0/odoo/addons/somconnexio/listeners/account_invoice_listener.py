from odoo.addons.component.core import Component

from bi_sc_client.services.notify_invoice_number import NotifyInvoiceNumber


class AccountInvoice(Component):
    _name = "account.invoice.listener"
    _inherit = "base.event.listener"
    _apply_on = ["account.invoice"]

    def on_record_write(self, record, fields=None):
        # TODO: filter only the client invoices?
        if "state" in fields and record.state == "open" and record.number:
            NotifyInvoiceNumber(record.number).run()
