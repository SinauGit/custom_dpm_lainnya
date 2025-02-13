from odoo import fields, models


class CompanySequence(models.Model):
    """Inherited Company for adding fields."""
    _inherit = 'res.company'

    customer_code = fields.Integer(string='Customer code', required=True,
                                   help='Add the required customer code.')
    next_code = fields.Integer(string='Next code', help='Expected next code')
