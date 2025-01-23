from odoo import api, fields, models, exceptions, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    total_qty = fields.Float(
        string='Total Quantity',
        compute='_compute_total_qty',
        store=True,
    )
    
    total_subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_total_subtotal',
        store=True,
        currency_field='currency_id',
    )

    total_discount_fixed = fields.Monetary(
        string='Total Disc.(Amount)',
        compute='_compute_total_discount_fixed',
        store=True,
        currency_field='currency_id',
    )

    subtotal_after_discount = fields.Monetary(
        string='Subtotal After Discount',
        compute='_compute_subtotal_after_discount',
        store=True,
        currency_field='currency_id',
    )

    tax_base_amount = fields.Monetary(
        string='Tax Base Amount',
        compute='_compute_tax_base_amount',
        store=True,
        currency_field='currency_id',
    )

    @api.depends('invoice_line_ids.quantity')
    def _compute_total_qty(self):
        for move in self:
            move.total_qty = sum(move.invoice_line_ids.mapped('quantity'))

    @api.depends('invoice_line_ids.quantity', 'invoice_line_ids.price_unit')
    def _compute_total_subtotal(self):
        for move in self:
            move.total_subtotal = sum(
                line.quantity * line.price_unit 
                for line in move.invoice_line_ids
            )

    @api.depends('invoice_line_ids.discount_fixed', 'invoice_line_ids.quantity')
    def _compute_total_discount_fixed(self):
        for move in self:
            total_discount = 0
            for line in move.invoice_line_ids:
                if line.discount_fixed:
                    total_discount += line.discount_fixed * line.quantity
            move.total_discount_fixed = total_discount

    @api.depends('total_subtotal', 'total_discount_fixed')
    def _compute_subtotal_after_discount(self):
        for move in self:
            move.subtotal_after_discount = move.total_subtotal - move.total_discount_fixed

    @api.depends('subtotal_after_discount')
    def _compute_tax_base_amount(self):
        for move in self:
            move.tax_base_amount = move.subtotal_after_discount * (11/12) if move.subtotal_after_discount else 0.0

    def button_draft(self):
        # Apply the override only for customer invoices
        for record in self:
            if record.move_type == 'out_invoice':  # Customer Invoice
                if not self.env.user.has_group('base.group_multi_company'):
                    raise exceptions.AccessError(_(
                        "You do not have the necessary permissions to reset to draft. "
                    ))
        # Call the original method
        return super().button_draft()
