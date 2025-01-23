from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'DPM %s' % (self.name)

    @api.depends('invoice_line_ids.subtotal_after_discount')
    def _compute_total_after_discount(self):
        for move in self:
            move.total_after_discount = sum(move.invoice_line_ids.mapped('subtotal_after_discount'))

    @api.depends('invoice_line_ids.tax_base_amount')
    def _compute_total_tax_base(self):
        for move in self:
            move.total_tax_base = sum(move.invoice_line_ids.mapped('tax_base_amount'))


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    subtotal_after_discount = fields.Monetary(
        string='Subtotal After Discount',
        compute='_compute_line_subtotal_after_discount',
        store=True,
        currency_field='currency_id',
        help="Total line setelah dikurangi diskon",
    )

    tax_base_amount = fields.Monetary(
        string='Tax Base Amount',
        compute='_compute_line_tax_base_amount',
        store=True,
        currency_field='currency_id',
        help="DPP PPN line (11/12 dari Subtotal After Discount)",
    )

    @api.depends('price_unit', 'quantity', 'discount', 'discount_fixed')
    def _compute_line_subtotal_after_discount(self):
        for line in self:
            line_total = line.price_unit * line.quantity
            discount_amount = (line_total * line.discount / 100.0)
            if line.discount_fixed:
                discount_amount += (line.discount_fixed * line.quantity)
            line.subtotal_after_discount = line_total - discount_amount

    @api.depends('subtotal_after_discount')
    def _compute_line_tax_base_amount(self):
        for line in self:
            line.tax_base_amount = (line.subtotal_after_discount * 11.0) / 12.0
