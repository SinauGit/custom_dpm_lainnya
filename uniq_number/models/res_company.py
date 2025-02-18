from odoo import fields, models


class CompanySequence(models.Model):
    """Inherited Company for adding fields."""
    _inherit = 'res.company'

    customer_code = fields.Integer(string='Customer code', required=True,
                                   help='Starting number for customer code.')
    vendor_code = fields.Integer(string='Vendor code', required=True,
                                   help='Starting number for vendor code.')
    next_customer_code = fields.Integer(string='Next Customer code', 
                                      help='Next number for customer code')
    next_vendor_code = fields.Integer(string='Next Vendor code', 
                                    help='Next number for vendor code')
