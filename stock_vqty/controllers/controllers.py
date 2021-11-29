# -*- coding: utf-8 -*-
from odoo import http

# class StockVqty(http.Controller):
#     @http.route('/stock_vqty/stock_vqty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_vqty/stock_vqty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_vqty.listing', {
#             'root': '/stock_vqty/stock_vqty',
#             'objects': http.request.env['stock_vqty.stock_vqty'].search([]),
#         })

#     @http.route('/stock_vqty/stock_vqty/objects/<model("stock_vqty.stock_vqty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_vqty.object', {
#             'object': obj
#         })