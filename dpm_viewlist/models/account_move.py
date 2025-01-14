from odoo import api, fields, models

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

    @api.depends('invoice_line_ids.discount_fixed')
    def _compute_total_discount_fixed(self):
        for move in self:
            move.total_discount_fixed = sum(
                line.discount_fixed 
                for line in move.invoice_line_ids
            ) 