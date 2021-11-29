# -*- coding: utf-8 -*-
from odoo import http

# class ProductVqty(http.Controller):
#     @http.route('/product_vqty/product_vqty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_vqty/product_vqty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_vqty.listing', {
#             'root': '/product_vqty/product_vqty',
#             'objects': http.request.env['product_vqty.product_vqty'].search([]),
#         })

#     @http.route('/product_vqty/product_vqty/objects/<model("product_vqty.product_vqty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_vqty.object', {
#             'object': obj
#         })