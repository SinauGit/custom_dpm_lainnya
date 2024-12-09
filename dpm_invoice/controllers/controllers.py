# -*- coding: utf-8 -*-
# from odoo import http


# class DpmInvoice(http.Controller):
#     @http.route('/dpm_invoice/dpm_invoice', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/dpm_invoice/dpm_invoice/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('dpm_invoice.listing', {
#             'root': '/dpm_invoice/dpm_invoice',
#             'objects': http.request.env['dpm_invoice.dpm_invoice'].search([]),
#         })

#     @http.route('/dpm_invoice/dpm_invoice/objects/<model("dpm_invoice.dpm_invoice"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('dpm_invoice.object', {
#             'object': obj
#         })

