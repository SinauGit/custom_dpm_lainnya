from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_unique_id = fields.Char(
        related='partner_id.unique_id',
        string='Vendor Code',
        store=True,
    )