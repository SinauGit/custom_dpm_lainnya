from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    discount_fixed = fields.Monetary(
        string="Discount (Amount)",
        default=0.0,
        currency_field="currency_id",
        help="Terapkan diskon dengan nominal tetap pada baris ini. Jumlah akan dikalikan "
        "dengan kuantitas produk.",
    )

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """Menyesuaikan perhitungan subtotal dengan mempertimbangkan diskon tetap."""
        done_lines = self.env['sale.order.line']
        for line in self:
            if float_is_zero(
                line.discount_fixed, precision_rounding=line.currency_id.rounding
            ):
                continue

            # Hitung diskon per unit
            discount = line._get_discount_from_fixed_discount()
            price = line.price_unit * (1 - (discount / 100.0))
            
            # Hitung total dengan mempertimbangkan kuantitas
            if line.tax_id:
                taxes = line.tax_id.with_context(
                    base_line=line,
                    discount=discount,
                ).compute_all(
                    price,
                    line.order_id.currency_id,
                    line.product_uom_qty,
                    product=line.product_id,
                    partner=line.order_id.partner_shipping_id,
                )
                line.update({
                    'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                    'price_total': taxes['total_included'],
                    'price_subtotal': taxes['total_excluded'],
                })
            else:
                subtotal = line.product_uom_qty * price
                line.update({
                    'price_tax': 0.0,
                    'price_total': subtotal,
                    'price_subtotal': subtotal,
                })
            
            done_lines |= line

        return super(SaleOrderLine, self - done_lines)._compute_amount()

    @api.onchange('discount_fixed')
    def _onchange_discount_fixed(self):
        """Menghitung persentase diskon berdasarkan nominal diskon tetap."""
        if self.env.context.get('ignore_discount_onchange'):
            return
        self = self.with_context(ignore_discount_onchange=True)
        self.discount = self._get_discount_from_fixed_discount()

    @api.onchange('discount')
    def _onchange_discount(self):
        """Menghitung nominal diskon tetap berdasarkan persentase diskon."""
        if self.env.context.get('ignore_discount_onchange'):
            return
        self = self.with_context(ignore_discount_onchange=True)

        if self.price_unit > 0:
            self.discount_fixed = (self.discount / 100.0) * self.price_unit
        else:
            self.discount_fixed = 0.0

    def _get_discount_from_fixed_discount(self):
        """Menghitung persentase diskon dari nominal diskon tetap."""
        self.ensure_one()
        currency = self.currency_id or self.company_id.currency_id
        if float_is_zero(self.discount_fixed, precision_rounding=currency.rounding):
            return 0.0
        if float_is_zero(self.price_unit, precision_rounding=currency.rounding):
            return 0.0
        return (self.discount_fixed / self.price_unit) * 100

    def _prepare_invoice_line(self, **optional_values):
        """Meneruskan nilai discount_fixed ke invoice line."""
        res = super()._prepare_invoice_line(**optional_values)
        res['discount_fixed'] = self.discount_fixed
        return res 