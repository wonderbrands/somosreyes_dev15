# -*- coding: utf-8 -*-
from odoo import http

# class MlmProduct(http.Controller):
#     @http.route('/mlm_product/mlm_product/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mlm_product/mlm_product/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mlm_product.listing', {
#             'root': '/mlm_product/mlm_product',
#             'objects': http.request.env['mlm_product.mlm_product'].search([]),
#         })

#     @http.route('/mlm_product/mlm_product/objects/<model("mlm_product.mlm_product"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mlm_product.object', {
#             'object': obj
#         })