# -*- coding: utf-8 -*-
from odoo import http

class CodebarSr(http.Controller):
    @http.route('/codebar_sr/codebar_sr/', auth='public')
    def index(self, **kw):
        return "Hola Mundo"

#     @http.route('/codebar_sr/codebar_sr/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('codebar_sr.listing', {
#             'root': '/codebar_sr/codebar_sr',
#             'objects': http.request.env['codebar_sr.codebar_sr'].search([]),
#         })

#     @http.route('/codebar_sr/codebar_sr/objects/<model("codebar_sr.codebar_sr"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('codebar_sr.object', {
#             'object': obj
#         })