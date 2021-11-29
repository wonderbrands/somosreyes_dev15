# -*- coding: utf-8 -*-

from odoo import models, fields, api

class shipping_cost(models.Model):
    _name = 'shipping_cost'

    name_marketplace = fields.Selection([('mercado_libre', 'Mercado Libre'), ('amazon', 'Amazon'),('linio', 'Linio'), ('walmart','Walmart'),('claroshop','ClaroShop'),('elektra','Elektra'),('liverpool','Liverpool'),('somos_reyes_shop','Somos Reyes Shop'), ('ebay','Ebay')],'Marketplace')
    name_seller = fields.Char('Seller')
    
    peso_volumetrico_inferior =  fields.Float('Peso Volumétrico Inferior (Kg)')
    peso_volumetrico_superior =  fields.Float('Peso Volumétrico Superior(kg)')

    descuento_fullfilment = fields.Float('Descuento Fullfilment(%)')

    descuento_otros = fields.Float('Descuento Otros(%)')

    descuento_x_precio_minimo = fields.Float('Descuento Precio Mínimo(%)')
    descuento_x_precio_maximo = fields.Float('Descuento Precio Máximo(%)')

    precio_minimo = fields.Float('Precio Mínimo de Producto')
    precio_maximo = fields.Float('Precio Máximo de Producto')

    shipping_price = fields.Float('Costo de Envío')

    tiempo_de_almacenamient0 = fields.Float('Tiempo de almacenamiento (días)')
    tarifa_de_almacenamiento_mes = fields.Float('Tarifa de almacenamiento (Mes)')
    tarifa_gestion_logistica  = fields.Float('Tarifa de Gestión logśtica')
    otros_costos  = fields.Float('Otros costos')
    asegurado = fields.Boolean('Asegurado')
    

	
    
   