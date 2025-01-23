from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'DPM %s' % (self.name)

    total_after_discount = fields.Monetary(
        string='Total After Discount',
        compute='_compute_total_after_discount',
        store=True,
        currency_field='currency_id',
    )

    total_tax_base = fields.Monetary(
        string='Total Tax Base',
        compute='_compute_total_tax_base',
        store=True,
        currency_field='currency_id',
    )

    @api.depends('invoice_line_ids.price_unit', 'invoice_line_ids.quantity', 
                'invoice_line_ids.discount', 'invoice_line_ids.discount_fixed')
    def _compute_total_after_discount(self):
        for move in self:
            total_before_discount = sum(
                line.price_unit * line.quantity 
                for line in move.invoice_line_ids
            )
            total_discount = sum(
                (line.price_unit * line.quantity * line.discount / 100.0) + 
                (line.discount_fixed * line.quantity if line.discount_fixed else 0)
                for line in move.invoice_line_ids
            )
            move.total_after_discount = total_before_discount - total_discount

    @api.depends('total_after_discount')
    def _compute_total_tax_base(self):
        for move in self:
            move.total_tax_base = (move.total_after_discount * 11.0) / 12.0


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    subtotal_after_discount = fields.Monetary(
        string='Subtotal After Discount',
        compute='_compute_line_subtotal_after_discount',
        store=True,
        currency_field='currency_id',
    )

    tax_base_amount = fields.Monetary(
        string='Tax Base Amount',
        compute='_compute_line_tax_base_amount',
        store=True,
        currency_field='currency_id',
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
