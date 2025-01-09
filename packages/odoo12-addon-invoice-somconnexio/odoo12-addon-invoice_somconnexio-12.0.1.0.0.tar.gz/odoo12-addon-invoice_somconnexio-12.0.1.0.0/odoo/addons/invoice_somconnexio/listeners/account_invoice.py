from odoo.addons.component.core import Component


class AccountInvoice(Component):
    _inherit = "account.invoice.listener"

    def on_record_write(self, record, fields=None):
        super().on_record_write(record, fields)
        if "b2_file_id" in fields:
            self.env["send.tokenized.invoice"].with_delay().send_tokenized_invoice(
                record
            )
