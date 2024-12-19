from odoo import models, api

class SaleDiscountWizard(models.TransientModel):
    _inherit = 'sale.order.discount'
    
    def action_apply_discount(self):
        """Override method asli untuk menambahkan update discount_fixed"""
        # Dapatkan sale order lines dari sale order terkait
        order = self.env['sale.order'].browse(self._context.get('active_id'))
        lines = order.order_line.filtered(lambda l: not l.display_type)
        
        # Konversi persentase ke nilai yang benar
        # Jika user input 10, pastikan tetap 10% (bukan 0.10%)
        percentage = float(self.discount_percentage)
        if percentage < 1.0:  # Jika kurang dari 1, berarti dalam desimal
            percentage = percentage * 100
        
        # Update discount_fixed setelah discount percentage diupdate
        for line in lines:
            if line.price_unit:
                # Hitung discount amount: (percentage/100) * price_unit
                # Contoh: 10% dari 1.990.000 = (10/100) * 1.990.000 = 199.000
                discount_fixed = (percentage / 100.0) * float(line.price_unit)
                
                vals = {
                    'discount_fixed': discount_fixed,
                    'discount': percentage,  # Simpan persentase yang benar
                    'primary_discount_type': 'percentage',
                    'original_discount': percentage,
                    'original_discount_fixed': discount_fixed,
                }
                line.write(vals)
        
        # Panggil super di akhir agar tidak menimpa nilai kita
        return super().action_apply_discount()

    @api.model
    def create(self, vals):
        # Pastikan context yang benar saat create
        return super(SaleDiscountWizard, self.with_context(
            no_recompute=True
        )).create(vals)