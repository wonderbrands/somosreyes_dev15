# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError
from odoo.tools.translate import _

class Inv_History(models.Model):
    _inherit = "product.template"
    sub_history_line_ids = fields.One2many('sub.history.lines', 'history_tmpl_ref_id', string='Historia')

class SubHistoryLines(models.Model):
    _name = "sub.history.lines"

    history_tmpl_ref_id = fields.Many2one('product.template', string='Referencia Historica')
    origen = fields.Char(string='Origen')
    ubicacion = fields.Char(string='Ubicación')
    fecha_movimiento =  fields.Datetime(string='Fecha de Movimiento')
    cantidad_entrada = fields.Integer ( 'Entrada')
    cantidad_salida = fields.Integer ( 'Salida')
    usuario =  fields.Char(string='Usuario')
    #usuario = fields.Many2one('res.users','Current User', default=lambda self: self.env.uid)

       