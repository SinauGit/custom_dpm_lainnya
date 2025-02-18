from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_unique_id = fields.Char(
        compute='_compute_partner_code',
        string='Customer Code',
        store=True,
    )
    
    @api.depends('partner_id', 'move_type')
    def _compute_partner_code(self):
        for move in self:
            if move.move_type in ('out_invoice', 'out_refund', 'out_receipt'):
                move.partner_unique_id = move.partner_id.customer_code
            else:
                move.partner_unique_id = move.partner_id.vendor_code