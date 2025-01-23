from odoo import api, fields, models

class AccountMove(models.Model):
    _inherit = "account.move"

    def _get_report_base_filename(self):
        self.ensure_one()
        return 'DPM %s' % (self.name)

    subtotal_after_discount = fields.Monetary(
        string='Subtotal After Discount',
        compute='_compute_subtotal_after_discount',
        store=True,
        currency_field='currency_id',
        help="Total setelah dikurangi diskon",
    )

    tax_base_amount = fields.Monetary(
        string='Tax Base Amount',
        compute='_compute_tax_base_amount',
        store=True,
        currency_field='currency_id',
        help="DPP PPN (11/12 dari Subtotal After Discount)",
    )

    @api.depends('invoice_line_ids.price_unit', 'invoice_line_ids.quantity', 
                'invoice_line_ids.discount', 'invoice_line_ids.discount_fixed')
    def _compute_subtotal_after_discount(self):
        for move in self:
            total_before_discount = 0
            total_discount = 0
            
            for line in move.invoice_line_ids:
                line_total = line.price_unit * line.quantity
                total_before_discount += line_total
                
                # Hitung total discount (percentage + fixed)
                discount_amount = (line_total * line.discount / 100.0)
                if line.discount_fixed:
                    discount_amount += (line.discount_fixed * line.quantity)
                total_discount += discount_amount
            
            move.subtotal_after_discount = total_before_discount - total_discount

    @api.depends('subtotal_after_discount')
    def _compute_tax_base_amount(self):
        for move in self:
            move.tax_base_amount = (move.subtotal_after_discount * 11.0) / 12.0
