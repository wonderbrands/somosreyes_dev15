# -*- coding: utf-8 -*-
from odoo import http

# class ShippingCost(http.Controller):
#     @http.route('/shipping_cost/shipping_cost/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/shipping_cost/shipping_cost/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('shipping_cost.listing', {
#             'root': '/shipping_cost/shipping_cost',
#             'objects': http.request.env['shipping_cost.shipping_cost'].search([]),
#         })

#     @http.route('/shipping_cost/shipping_cost/objects/<model("shipping_cost.shipping_cost"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('shipping_cost.object', {
#             'object': obj
#         })