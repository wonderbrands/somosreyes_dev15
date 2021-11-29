# -*- coding: utf-8 -*-
from odoo import http

# class PurchaseVqty(http.Controller):
#     @http.route('/purchase_vqty/purchase_vqty/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_vqty/purchase_vqty/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_vqty.listing', {
#             'root': '/purchase_vqty/purchase_vqty',
#             'objects': http.request.env['purchase_vqty.purchase_vqty'].search([]),
#         })

#     @http.route('/purchase_vqty/purchase_vqty/objects/<model("purchase_vqty.purchase_vqty"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_vqty.object', {
#             'object': obj
#         })