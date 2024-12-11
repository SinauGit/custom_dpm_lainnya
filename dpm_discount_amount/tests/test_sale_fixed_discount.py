from odoo import api, fields, models
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged('post_install', '-at_install')
class TestSaleFixedDiscount(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Partner'})
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'type': 'consu',
        })
        self.tax = self.env['account.tax'].create({
            'name': 'Tax 10%',
            'amount': 10,
            'amount_type': 'percent',
        })

    def test_fixed_discount_without_tax(self):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 100.0,
                'discount_fixed': 10.0,
            })]
        })
        
        line = order.order_line[0]
        self.assertEqual(line.discount, 10.0)  # 10.0 dari 100.0 = 10%
        self.assertEqual(line.price_subtotal, 90.0)

    def test_fixed_discount_with_quantity(self):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 2,
                'price_unit': 100.0,
                'discount_fixed': 10.0,
            })]
        })
        
        line = order.order_line[0]
        self.assertEqual(line.discount, 10.0)
        self.assertEqual(line.price_subtotal, 180.0)  # (100 - 10) * 2

    def test_fixed_discount_with_tax(self):
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 1,
                'price_unit': 100.0,
                'discount_fixed': 10.0,
                'tax_id': [(6, 0, [self.tax.id])],
            })]
        })
        
        line = order.order_line[0]
        self.assertEqual(line.price_subtotal, 90.0)
        self.assertEqual(line.price_total, 99.0)  # 90 + (90 * 0.10)