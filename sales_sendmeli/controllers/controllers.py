# -*- coding: utf-8 -*-
from odoo import http

# class SalesVqty(http.Controller):
#     @http.route('/sales_vqty/sales_vqty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sales_vqty/sales_vqty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sales_vqty.listing', {
#             'root': '/sales_vqty/sales_vqty',
#             'objects': http.request.env['sales_vqty.sales_vqty'].search([]),
#         })

#     @http.route('/sales_vqty/sales_vqty/objects/<model("sales_vqty.sales_vqty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sales_vqty.object', {
#             'object': obj
#         })