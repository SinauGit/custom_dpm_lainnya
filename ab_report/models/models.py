from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from terbilang import Terbilang
t = Terbilang()


class AccountBankStatement(models.Model):
    _inherit = "account.bank.statement"

    total_amount = fields.Monetary(string='Total Amount', readonly=True,compute='_compute_total_amount')
    # number = fields.Char(string='Number',compute='get_number',store=True,default='/')
    

    @api.depends('line_ids.amount')
    def _compute_total_amount(self):
        for rec in self:
            total_amount = 0.0
            for line in rec.line_ids:
                total_amount += line.amount
            rec.total_amount = total_amount
    
    def terbilang(self,val):
        t.parse(val)
        return t.getresult().title()

    @api.depends('journal_id')
    def get_number(self):
        number = '/'
        if self.number == '/' and self.journal_id:
            number = self.env['ir.sequence'].next_by_code('patty.cash.seq') or '/'            
            number = number.replace('kode_journal',self.journal_id.code)
        self.number = number


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    reconciler_id = fields.Many2one('res.users', string='User Reconciler'
                                    )
    # number = fields.Char(string='Number',compute='get_number',store=True,default='/')
    # journal_sequence = fields.Char(comodel_name='account.journal', string='Account Journal Sequence', related='journal_id.code')
    
    # @api.depends('journal_sequence')
    # def get_number(self):
    #     # self.ensure_one()
    #     for x in self:
    #         number = '/'
    #         if x.number == '/' and self.journal_sequence:
    #             print ('asdddddddddddsssssssssssssaaaaaaaaaaaaaa')
    #             number = self.env['ir.sequence'].next_by_code('patty.cash.line.seq') or '/'            
    #             print(number,'==================')
    #             number = number.replace('kode_journal',x.journal_sequence)
    #             print (number,'==================')
    #         x.number = number

    
    def action_print_patty(self):
        self.ensure_one()        
        action = self.env.ref('ab_report.action_report_patty_cash').report_action(self)        
        return action


    
    # @api.model
    # def create(self, vals):
    #     print(self.env.context)
    #     print(vals)
    #     # if vals.get('name', '/') == '/':
    #     res = super(AccountBankStatement, self).create(vals)
    #     # print(vals,'============')
    #     number = self.env['ir.sequence'].next_by_code('patty.cash.seq') or '/'
    #     # if vals.get('journal_id'):
    #     #     journal = self.env['account.journal'].browse(vals['journal_id'])
    #     print (res)
    #     print  (res.journal_id)

    #     # number = number.replace('kode_journal',res.journal_id.code)
    #     # # vals['number'] = number
    #     # res.number = number
    #     return res

    def write(self, vals):
        res = super(AccountBankStatementLine, self).write(vals)
        for rec in self:
            if rec.is_reconciled:
                if not self.env.context.get('update_reconciler'):
                    rec.with_context(update_reconciler=True).reconciler_id = self.env.user.id
        return res


class StockLot(models.Model):
    _inherit = 'stock.lot'

    @api.constrains('name', 'company_id')
    def _check_unique_lot(self):
        super()._check_unique_lot()
        domain = [
            ('name', '=', self.mapped('name')),
            ('company_id', '=', self.company_id.ids),
        ]
        fields = ['company_id', 'name']
        groupby = ['company_id', 'name']
        records = self._read_group(domain, fields, groupby, lazy=False)
        for rec in records:
            if rec['__count'] > 1:
                raise ValidationError("Lot/Serial Number must be unique across a company!")
