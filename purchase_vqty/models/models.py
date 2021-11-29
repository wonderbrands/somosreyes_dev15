# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import Warning 
import json
import requests
import subprocess
from multiprocessing import Process, current_process

import sys


def update_product_venti(sku, stock_mercadolibre, stock_linio, stock_amazon, stock_prestashop, stock_walmart, stock_claroshop, access_token_venti):
	try:
		_logger = logging.getLogger(__name__)

		headers={"content-type":"application/json","Authorization":"bearer "+ access_token_venti}
		body={
				"sku": sku,
				"channelData": [
					{
						"channel": "mercadolibre",
						"quantity": stock_mercadolibre
					},
					{
						"channel": "linio",
						"quantity":stock_linio
					},
					{
						"channel": "amazon",
						"quantity":stock_amazon
					},
					{
						"channel": "prestashop",
						"quantity": stock_prestashop
					}, 
					{
						"channel": "walmart",
						"quantity": stock_walmart
					}, 
					{
						"channel": "claroshop",
						"quantity": stock_claroshop
					}, 
				]
			}

		url='https://ventiapi.azurewebsites.net/api/stock/updatepricestockbychannel'
		r=requests.post(url, headers=headers, data= json.dumps(body) )
		_logger.info('PURCHASE SKU: %s Meli %s |  Linio %s |Amazon %s |Prestashop %s |Walmart %s |ClaroShop %s en Venti.', sku, str(stock_mercadolibre), str(stock_linio), str(stock_amazon), str(stock_prestashop), str(stock_walmart), str(stock_claroshop) )
		_logger.info('PURCHASE Respuesta Venti: %s ', r.text )  
		process_name =  current_process().name
		_logger.info('Process name: %s ', process_name ) 


	except Exception as e:
		_logger.error('Error en purchase_vqty.update_product_venti(): %s', str (e))


class purchase_vqty(models.Model):
	_inherit = 'purchase.order'

	#@api.multi
	def button_confirm(self):
		_logger = logging.getLogger(__name__)

		lines = len(self.order_line.ids)

		#--- Obtenemos el Token de venti
		access_token_venti = self.env['tokens_markets.tokens_markets'].search([['name_marketplace','=', 'VENTI' ]]).access_token

		ids_product=[]
		vqty_product=[]
		products_stock_real=[]
		skus_product =[]

		for x in range(lines):
			#--- Recuperados el Id del Producto en Odoo
			ids_product.append(self.order_line[x].product_id.id)
			id_product = self.order_line[x].product_id.id

			#--- Recuperamos el Sku de cada producto en Odoo
			default_code = self.env['product.product'].search([['id', '=', id_product ]]).default_code
			sku = self.env['product.product'].search([['id', '=', id_product ]]).default_code
			
			skus_product.append(default_code)

			#--- Recuperamos la Cantidad Pronosticada
			virtual_available = self.env['product.product'].search([['id', '=', id_product ]]).virtual_available
			vqty_product.append(virtual_available)
			#--- Recuperamos el Stock Real que tiene Somos Reyes
			stock_real = self.env['product.product'].search([['id', '=', id_product ]]).stock_real
			products_stock_real.append(stock_real)

			#--- Recuperamos el sctock de exclusivas
			stock_exclusivas = self.env['product.product'].search([['id', '=', id_product ]]).stock_exclusivas
			#--- Recuperamos el stock de Urrea
			stock_urrea = self.env['product.product'].search([['id', '=', id_product ]]).stock_urrea

			#--- Recuperamos el stock_markets.
			stock_markets_actual = self.env['product.product'].search([['id', '=', id_product ]]).stock_markets 

			#--- Recuperamos la cantidad que se hace de este producto en el pedido actual (self)
			product_uom_qty = self.order_line[x].product_uom_qty

			#--- calculamos la cantidad pronosticada para actualizar en meli, para cada marketplace. SUMA ENTRADA
			stock_markets_nuevo = int(stock_real)+int(stock_exclusivas)+int(stock_urrea) + int(product_uom_qty)
			
			#if stock_markets_actual ==0:
			#	stock_markets_nuevo = int(stock_real)+int(stock_exclusivas)+int(stock_urrea) + int(product_uom_qty)
			#else:
			#	stock_markets_nuevo = int(stock_markets_actual) + int(product_uom_qty)

			#---Calculamos politicas de stock para cada marketplace
			stock_mercadolibre =  int(stock_real + stock_exclusivas + stock_urrea + product_uom_qty)
			stock_linio = int(stock_real + stock_exclusivas + stock_urrea + product_uom_qty)
			stock_amazon = int(stock_real + stock_exclusivas + stock_urrea + product_uom_qty)
			stock_prestashop = int(stock_real + stock_exclusivas + stock_urrea + product_uom_qty)
			stock_walmart = int(stock_real + stock_exclusivas  + product_uom_qty)
			stock_claroshop = int(stock_real + stock_exclusivas + stock_urrea + product_uom_qty)
			
			_logger.info('ENTRADA| Id: %s | SKU:  %s | stock_real: %s | product_uom_qty:%s |stock_markets_nuevo : %s', str(id_product), str(sku) , str(stock_real),str(product_uom_qty),str(stock_markets_nuevo) )
			_logger.info('ENTRADA Meli: %s| Linio: %s | Amazon:  %s | Prestashop: %s |Walmart : %s |Claroshop: %s ',str(stock_mercadolibre), str(stock_linio), str(stock_amazon), str(stock_prestashop), str(stock_walmart), str(stock_claroshop))
			
			update_product_venti(sku, stock_mercadolibre, stock_linio, stock_amazon, stock_prestashop, stock_walmart, stock_claroshop, access_token_venti)
			
			_logger.info('SE ACTUALIZO VENTI')
			#---Actualizamos el campo stock_markets del Producto
			producto = self.env['product.product'].search([('id', '=',id_product )]) 
			producto.write({'stock_markets': stock_markets_nuevo})

		rec = super(purchase_vqty, self).button_confirm()

		return rec