from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """Inherited Partner fo generating unique sequence."""
    _inherit = 'res.partner'

    customer_code = fields.Char(string='Customer Code', help="Unique code for customer",
                            readonly=False, default='', copy=False)
    vendor_code = fields.Char(string='Vendor Code', help="Unique code for vendor",
                            readonly=False, default='', copy=False)

    _sql_constraints = [
        ('customer_code_uniq', 'UNIQUE(customer_code)', 
         'Customer Code must be unique! This code is already used by another customer.'),
        ('vendor_code_uniq', 'UNIQUE(vendor_code)', 
         'Vendor Code must be unique! This code is already used by another vendor.')
    ]

    @api.constrains('customer_code', 'vendor_code')
    def _check_unique_codes(self):
        for record in self:
            if record.customer_code and record.customer_code != '/':
                duplicate = self.search([
                    ('customer_code', '=', record.customer_code),
                    ('id', '!=', record.id)
                ])
                if duplicate:
                    raise ValidationError(_('The Customer Code must be unique! This code is already used by %s') % duplicate.name)
            
            if record.vendor_code and record.vendor_code != '/':
                duplicate = self.search([
                    ('vendor_code', '=', record.vendor_code),
                    ('id', '!=', record.id)
                ])
                if duplicate:
                    raise ValidationError(_('The Vendor Code must be unique! This code is already used by %s') % duplicate.name)

    @api.model
    def create(self, values):
        """Super create function for generating sequence."""
        res = super(ResPartner, self).create(values)
        company = self.env.company.sudo()
        
        # Generate customer code
        if res.customer_rank > 0 and res.customer_code == '/':
            if company.next_customer_code:
                res.customer_code = 'C' + str(company.next_customer_code)
                company.write({'next_customer_code': company.next_customer_code + 1})
            else:
                res.customer_code = 'C' + str(company.customer_code)
                company.write({'next_customer_code': company.customer_code + 1})
        
        # Generate vendor code
        if res.supplier_rank > 0 and res.vendor_code == '/':
            if company.next_vendor_code:
                res.vendor_code = 'V' + str(company.next_vendor_code)
                company.write({'next_vendor_code': company.next_vendor_code + 1})
            else:
                res.vendor_code = 'V' + str(company.vendor_code)
                company.write({'next_vendor_code': company.vendor_code + 1})
        
        return res
