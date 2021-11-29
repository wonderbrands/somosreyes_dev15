# -*- coding: utf-8 -*-
from odoo import http

# class Sohelpdesk(http.Controller):
#     @http.route('/sohelpdesk/sohelpdesk/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sohelpdesk/sohelpdesk/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sohelpdesk.listing', {
#             'root': '/sohelpdesk/sohelpdesk',
#             'objects': http.request.env['sohelpdesk.sohelpdesk'].search([]),
#         })

#     @http.route('/sohelpdesk/sohelpdesk/objects/<model("sohelpdesk.sohelpdesk"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sohelpdesk.object', {
#             'object': obj
#         })