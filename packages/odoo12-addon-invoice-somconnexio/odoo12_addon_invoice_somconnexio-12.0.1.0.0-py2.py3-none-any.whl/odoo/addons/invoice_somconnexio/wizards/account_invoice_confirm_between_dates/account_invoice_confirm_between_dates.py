from odoo import api, fields, models

from odoo.addons.queue_job.job import identity_exact


class AccountInvoiceConfirmBetweenDates(models.TransientModel):
    _name = "account.invoice.confirm.between.dates"

    start_date = fields.Date("Start date")
    end_date = fields.Date("End date")

    @api.multi
    def run_wizard(self):
        # Select all invoices between start and end date in draft state
        invoices = self.env["account.invoice"].search(
            [
                ("state", "=", "draft"),
                ("date_invoice", ">=", self.start_date),
                ("date_invoice", "<=", self.end_date),
                ("type", "in", ("out_invoice", "out_refund")),
                ("release_capital_request", "=", False),
            ]
        )
        # Confirm invoices with the account_invoice_confirm wizard
        for invoice in invoices:
            invoice.with_delay(
                priority=30,
                identity_key=identity_exact,
            ).action_invoice_open_job()
