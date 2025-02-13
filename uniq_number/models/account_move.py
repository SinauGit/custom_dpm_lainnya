from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_unique_id = fields.Char(
        related='partner_id.unique_id',
        string='Customer Code',
        store=True,
    ) 