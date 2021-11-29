# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import Warning 
import json
import requests


class sales_autonoma(models.Model):
    _inherit = 'sale.order'

    #@api.multi
    def ejecuta_procesos(self):
        _logger = logging.getLogger(__name__)
        _logger.info('Ejecutando procesos')

        self.action_confirm() #--- Ejecuta el Boton de Confirmar
        picking_ids =  self.picking_ids
        _logger.info('Picking IDs: %s', picking_ids)
        picking_id=0
        for picking in picking_ids:
        	 _logger.info('ID:%s, Nombre %s',  picking.id, picking.name)
        	 if 'PICK' in picking.name:
        	 	picking_id = picking.id
  
        return dict ( {
              'name': _('Procesar Operación :Picking'),
              'view_type': 'form',
              "view_mode": 'form',
              'res_model': 'stock.picking',
              'type': 'ir.actions.act_window',
              'res_id': picking_id, 
              'target': 'new',
              }  )
        
