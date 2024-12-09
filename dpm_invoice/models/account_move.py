from odoo import models

class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'DPM %s' % (self.name)
