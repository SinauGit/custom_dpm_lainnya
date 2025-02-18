from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Related fields untuk kedua kode
    customer_code = fields.Char(related='partner_id.customer_code', store=True)
    vendor_code = fields.Char(related='partner_id.vendor_code', store=True)

    # Field utama yang dikondisikan
    partner_unique_id = fields.Char(
        string='Customer/Vendor Code',
        compute='_compute_partner_unique_id',
        store=True
    )

    @api.depends('move_type', 'customer_code', 'vendor_code')
    def _compute_partner_unique_id(self):
        for move in self:
            if move.move_type in ('out_invoice', 'out_refund', 'out_receipt'):
                move.partner_unique_id = move.customer_code
            elif move.move_type in ('in_invoice', 'in_refund', 'in_receipt'):
                move.partner_unique_id = move.vendor_code
            else:
                move.partner_unique_id = False
