# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, exceptions, models, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.exceptions import ValidationError
from PIL import Image
import io
import base64


class codebar_pr(models.Model):
    _name = 'codebar_pr'
    _rec_name = 'operacion'
    _description ='Productos de Operación'

    operacion = fields.Char(string='Operación')
    upc = fields.Char(string='UPC')
    nombre_producto = fields.Char(string='Producto', compute='_get_product', store = True) # Obtener nombre del producto del UPC
    cantidad_pedida = fields.Integer(string='Cantidad pedida',compute='_get_product', store = True) # Obtener la cantidad de la operacion
    cantidad_disponible = fields.Integer(string='Cantidad disponible',compute='_get_product', store = True) # Checar el Stock del producto
    cantidad_hecha = fields.Integer(string='Cantidad por hacer') # Permitir cambiar cantidad hacia abajo
    fecha_operacion = fields.Datetime(string='Fecha Operacion',default=lambda self: fields.datetime.now())
    imagen_producto = fields.Binary()

    @api.model
    def create(self, vals):
        _logger = logging.getLogger(__name__)
        _logger.info('NOMBRE DEL MOVIMIENTO:%s', self.operacion)

        _logger.info('VALORES:%s', vals)
        cantidad_pedida_actualizar = vals['cantidad_pedida']
        cantidad_disponible_actualizar = vals['cantidad_disponible']
        cantidad_hecha = vals['cantidad_hecha']
        operacion = vals['operacion']

        move_id = self.env['stock.picking'].search([('name','=',operacion)]).move_ids_without_package.id
        _logger.info('MOVE ID VALS :%s, ',move_id)
        operacion_a_actualizar = self.env['stock.move'].search([('id', '=', move_id)] )
        update_operacion = operacion_a_actualizar.write({'product_uom_qty':cantidad_pedida_actualizar,'availability':cantidad_disponible_actualizar ,'quantity_done': cantidad_hecha, 'state':'done' })
        _logger.info('ACTUALIZO MOVIMIENTO:%s', update_operacion)
        return super(codebar_pr, self).create(vals)
    
    #@api.multi
    @api.depends('upc')
    def _get_product(self):
        _logger = logging.getLogger(__name__)
        _logger.info ('UPC:'+ str(self.upc) )
        try:
            if self.upc:
                producto = self.env['product.template'].search([('barcode','=',self.upc)]).display_name
                _logger.info('PRODUCTO: %s ',  producto)
                self.nombre_producto = producto
               
                move_id = self.env['stock.picking'].search([('name','=',self.operacion)]).move_ids_without_package.id
                move_name = self.env['stock.picking'].search([('name','=',self.operacion)]).name

                _logger.info('ID OPERACION: %s , NOMBRE OPERACION: %s',  move_id,move_name )

                datos_operacion = self.env['stock.move'].search_read([('id', '=', move_id)])
                #_logger.info('DATOS OPERACION: %s ',  datos_operacion )

                
                cantidad_pedida = datos_operacion[0]['product_uom_qty']
                self.cantidad_pedida = cantidad_pedida

                cantidad_disponible = datos_operacion[0]['availability']
                self.cantidad_disponible = cantidad_disponible

                  
                base64_string = self.env['product.product'].search([('barcode','ilike',self.upc)]).image_medium
                _logger.info('IMAGEN PRODUCTO: %s ',  base64_string )

                #base64_string=b'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'
                #imagen_producto = base64_to_image(base64_string)
                #_logger.info('IMAGEN PRODUCTO: %s ',  imagen_producto )
                self.imagen_producto = base64_string

                _logger.info('CANTIDADES Pedida:%s, Disponible:%s', cantidad_pedida, cantidad_disponible )


        except Exception as e:
            _logger.info ('_get_product(): %s '+ str(e) ) 

        
    

    
           
    @api.onchange('cantidad_hecha')
    def onchange_cantidad_hecha(self):
        _logger = logging.getLogger(__name__)
        _logger.info('Cantidad hecha:%s', self.cantidad_hecha)
        if self.upc:
            if self.cantidad_hecha > self.cantidad_pedida:
                raise exceptions.ValidationError('La Cantidad por Hacer, es Mayor a la Cantidad Pedida')
            elif self.cantidad_hecha == 0:
                raise exceptions.ValidationError('La Cantidad por Hacer no puede ser Cero')
            else:
                pass

        #value={''}
        #self.write(values)
    






    
    
        