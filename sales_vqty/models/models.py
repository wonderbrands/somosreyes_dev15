# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import Warning 
import json
import requests


def update_product_venti(sku, stock_mercadolibre, stock_linio, stock_amazon, stock_prestashop, stock_walmart, stock_claroshop, access_token_venti):
	try:
		_logger = logging.getLogger(__name__)
		headers={"content-type":"application/json","Authorization":"bearer "+ access_token_venti}
		body={
		        "sku": sku,
				"channelData": [
					{
						"channel": "mercadolibre",
						"quantity": int(stock_mercadolibre)
						#"price": 155.40
					},
					{
						"channel": "linio",
						"quantity":int(stock_linio)
					},
					{
						"channel": "amazon",
						"quantity":int(stock_amazon)
					},
					{
						"channel": "prestashop",
						"quantity": int(stock_prestashop)
					}, 
					{
						"channel": "walmart",
						"quantity": int(stock_walmart)
					}, 
					{
						"channel": "claroshop",
						"quantity": int(stock_claroshop)
					}, 
				]
			}

		url='https://ventiapi.azurewebsites.net/api/stock/updatepricestockbychannel'
		r=requests.post(url, headers=headers, data= json.dumps(body) )
		_logger.info('SALES SKU: %s Meli %s |  Linio %s |Amazon %s |Prestashop %s |Walmart %s |ClaroShop %s en Venti.', sku, str(stock_mercadolibre), str(stock_linio), str(stock_amazon), str(stock_prestashop), str(stock_walmart), str(stock_claroshop) )
		_logger.info('SALES Respuesta Venti: %s ', r.text )  

	except Exception as e:
		_logger.error('Error en update_product_venti(): %s', str (e))


class sales_vqty(models.Model):
	_inherit = 'sale.order'

	@api.multi
	def action_confirm(self):
		_logger = logging.getLogger(__name__)
		# Solo para aquellas Ordenes de venta que no provengan de la generación automática por API
		# Hasta el momento solo tenemos implementado La funcionalidad para Mercado Libre.

		marketplace_order_id = self.marketplace_order_id
		marketplace = str(self.marketplace)
		#_logger.info('marketplace_order_id: '+str(marketplace_order_id)+' marketplace:'+str(marketplace) )


		if 'MERCADO LIBRE' in marketplace and ( marketplace_order_id == True or marketplace_order_id !=''):
			_logger = logging.getLogger(__name__)
			_logger.info('Orden de Mercado Libre, la existencia ya fue calculada, actualizada en odoo y notificada a Venti.')
			rec = super(sales_vqty, self).action_confirm()	
			return rec

		elif 'LINIO' in marketplace or 'AMAZON' in marketplace or 'LIVERPOOL' in marketplace or 'WALMART' in marketplace or 'CLARO' in marketplace or '' in marketplace: 
			_logger = logging.getLogger(__name__)
			sale_order_name = len(self.order_line.ids)
			lines = len(self.order_line.ids)

			#--- Verifiquemos cual es el Seller  en la Orden de Ventas
			seller_marketplace =  self.seller_marketplace

			#--- Obtenemos el Token de ese Seller Id
			access_token_venti = self.env['tokens_markets.tokens_markets'].search([['name_marketplace','=', 'VENTI' ]]).access_token

			ids_product=[]
			vqty_product=[]
			skus_product =[]
			products_stock_real=[]

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
				#--- Recuperamos el stock de Markets
				stock_markets_actual = self.env['product.product'].search([['id', '=', id_product ]]).stock_markets

				#--- Recuperamos la cantidad que se hace de este producto en el pedido actual (self)
				product_qty = self.order_line[x].product_qty

				#--- calculamos la cantidad pronosticada para actualizar en meli, para cada marketplace. 
				stock_markets_nuevo = int(stock_real)+int(stock_exclusivas)+int(stock_urrea) - int(product_qty) 
				#if stock_markets_actual == 0:
				#	stock_markets_nuevo = int(stock_real)+int(stock_exclusivas)+int(stock_urrea) - int(product_qty) 
				#else:
				#	stock_markets_nuevo = int(stock_markets_actual) - int(product_qty) 

				#---Calculamos politicas de stock para cada marketplace
				stock_mercadolibre =  stock_real + stock_exclusivas + stock_urrea - product_qty
				stock_linio = stock_real + stock_exclusivas  - product_qty
				stock_amazon = stock_real + stock_exclusivas + stock_urrea - product_qty
				stock_prestashop = stock_real + stock_exclusivas + stock_urrea  - product_qty 
				stock_walmart = stock_real + stock_exclusivas  - product_qty
				stock_claroshop = stock_real + stock_exclusivas + stock_urrea  - product_qty
			
				_logger.info('SALES | Id: %s | SKU:  %s | stock_real: %s | product_qty:%s |stock_markets_nuevo : %s', str(id_product), str(sku) , str(stock_real),str(product_qty),str(stock_markets_nuevo) )
				_logger.info('SALES Meli: %s| Linio: %s | Amazon:  %s | Prestashop: %s |Walmart : %s |Claroshop: %s ',str(stock_mercadolibre), str(stock_linio), str(stock_amazon), str(stock_prestashop), str(stock_walmart), str(stock_claroshop))
				#update_product_venti(sku, stock_mercadolibre, stock_linio, stock_amazon, stock_prestashop, stock_walmart, stock_claroshop, access_token_venti)
				
				#---Actualizamos el campo stock_markets del Producto

				producto = self.env['product.product'].search([('id', '=',id_product )])
				producto.write({'stock_markets': stock_markets_nuevo})
			
			rec = super(sales_vqty, self).action_confirm()	

		return rec
