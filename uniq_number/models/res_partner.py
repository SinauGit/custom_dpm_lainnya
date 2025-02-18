from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    """Inherited Partner fo generating unique sequence."""
    _inherit = 'res.partner'

    unique_id = fields.Char(string='Customer/Vendor Code', help="The Unique Sequence no",
                            readonly=False, default='/', copy=False)

    _sql_constraints = [
        ('unique_id_uniq', 'UNIQUE(unique_id)', 
         'Customer Code must be unique! This code is already used by another customer/vendor.')
    ]

    @api.constrains('unique_id')
    def _check_unique_id(self):
        for record in self:
            if record.unique_id and record.unique_id != '/':
                duplicate = self.search([
                    ('unique_id', '=', record.unique_id),
                    ('id', '!=', record.id)
                ])
                if duplicate:
                    raise ValidationError(_('The Customer/Vendor Code must be unique! This code is already used by %s') % duplicate.name)

    @api.model
    def create(self, values):
        """Super create function for generating sequence."""
        res = super(ResPartner, self).create(values)
        company = self.env.company.sudo()
        if res.customer_rank > 0 and res.unique_id == '/':
            if company.next_code:
                res.unique_id = company.next_code
                res.name = '[' + str(company.next_code) + ']' + str(
                    res.name)
                company.write({'next_code': company.next_code + 1})
            else:
                res.unique_id = company.customer_code
                res.name = '[' + str(company.customer_code) + ']' + str(
                    res.name)
                company.write({'next_code': company.customer_code + 1})
        return res
