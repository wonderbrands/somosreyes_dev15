# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api, _
from odoo.exceptions import Warning 
from datetime import datetime
import logging
import json
import requests


class product_stock(models.Model):
    _inherit = 'product.template'
    _rec_name = 'fraccion_arancelaria'
    _description = "Campos de Importacion comercial"

    fraccion_arancelaria =  fields.Char("Fracción Arancelaria")
    porcentaje_importacion =  fields.Float(string='Porcentaje Impuesto Importación', help="Porcentaje Impuesto de Importación")
    nom = fields.Char(string='NOMS', help="Norma Oficial éxicana para Comercio Exterior")
    costo_dolares_actual = fields.Monetary(string="Costo actual USD")
    costo_dolares_anterior = fields.Monetary(string="Costo anterior USD")
    tipo_de_cambio = fields.Monetary(string="Tipo de cambio")
    fabricante =  fields.Char("Fabricante")
       
