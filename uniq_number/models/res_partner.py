from odoo import models, fields, api


class ResPartner(models.Model):
    """Inherited Partner fo generating unique sequence."""
    _inherit = 'res.partner'

    unique_id = fields.Char(string='Unique Id', help="The Unique Sequence no",
                            readonly=False, default='/')

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
