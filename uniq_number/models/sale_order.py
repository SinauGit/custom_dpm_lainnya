from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_unique_id = fields.Char(
        related='partner_id.unique_id',
        string='Customer Code',
        store=True,
    ) 