# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning 

class sohelpdesk(models.Model):
    _inherit = 'helpdesk.ticket'
    so_name = fields.Char(string='Orden de Venta asociado') 
    ordermp_id = fields.Char(string='Orden de Venta del Marketplace', compute='_total' )

    #@api.one
    @api.depends('so_name')
    def _total(self):
        name = self.so_name
        self.ordermp_id = self.env['sale.order'].search([['name', '=', name ]]).marketplace_order_id
        


