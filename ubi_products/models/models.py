# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import Warning 

class Ubi_products(models.Model):
    _name = 'ubi_products'
    _description = 'Ubicaciones de Productos'
    _rec_name = 'ubicacion'
    
    ubicacion = fields.Char('Ubicación', required=True, help='Introduce un nombre de la Ubicación')
    
