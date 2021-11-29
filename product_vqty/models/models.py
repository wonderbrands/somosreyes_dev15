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
						"quantity":int(stock_linio),
					},
					{
						"channel": "amazon",
						"quantity":int(stock_amazon),
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
		_logger.info('SKU: %s Meli %s |  Linio %s |Amazon %s |Prestashop %s |Walmart %s |ClaroShop %s en Venti.', sku, str(stock_mercadolibre), str(stock_linio), str(stock_amazon), str(stock_prestashop), str(stock_walmart), str(stock_claroshop) )
		_logger.info('Respuesta Venti: %s ', r.text )  

	except Exception as e:
		_logger.error('Error en update_product_venti(): %s', str (e))


class product_vqty(models.Model):
	_inherit = 'product.template'

	@api.model
	def create(self, values):
		"""Override default Odoo create function and extend."""
		# Do your custom logic here
		raise Warning(_("Id Producto: %s" %self.values))
		return super(product_vqty, self).create(values)

	#@api.multi
	def write(self, vals):
		_logger = logging.getLogger(__name__)
		id_product = self.id
		raise Warning(_("Id Producto: %s" %self.id))
		#_logger.info('Id del Producto: %s', str(id_product) )

		try:
			id_product = self.id
			combo = self.combo
			_logger.info('Valores: %s|', str(vals) )
			'''
			#--- Recuperamos la Cantidad Pronosticada
			virtual_available = self.env['product.product'].search([['id', '=', id_product ]]).virtual_available
			#--- Recuperamos el sctock de exclusivas
			stock_exclusivas = self.env['product.product'].search([['id', '=', id_product ]]).stock_exclusivas
			#--- Recuperamos el stock de Urrea
			stock_urrea = self.env['product.product'].search([['id', '=', id_product ]]).stock_urrea

			#--- Recuperamos la cantidad que se hace de este producto en el pedido actual (self)
			product_qty = self.order_line[x].product_qty

			#--- calculamos la cantidad pronosticada para actualizar en meli, para cada marketplace. 
			quantity = int(virtual_available)

			#---Calculamos politicas de stock para cada marketplace
			stock_mercadolibre =  quantity + int(stock_exclusivas) + int(stock_urrea)
			stock_linio = quantity + int(stock_exclusivas) 
			stock_amazon = quantity + int(stock_exclusivas) + int(stock_urrea)
			stock_prestashop = quantity + int(stock_exclusivas) + int(stock_urrea)
			stock_walmart = quantity + int(stock_exclusivas) 
			stock_claroshop = quantity + int(stock_exclusivas) + int(stock_urrea)

			
			_logger.info('Seller Marketplace: %s| Id: %s | SKU:  %s | Pronosticada: %s |Token : %s',str(seller_marketplace), str(id_product), str(sku) , str(quantity), access_token_venti )
			_logger.info('Meli: %s| Linio: %s | Amazon:  %s | Prestashop: %s |Walmart : %s |Claroshop: %s ',str(stock_mercadolibre), str(stock_linio), str(stock_amazon), str(stock_prestashop), str(stock_walmart), str(stock_claroshop))
			#update_product_venti(sku, quantity, access_token_venti)
			update_product_venti(sku, stock_mercadolibre, stock_linio, stock_amazon, stock_prestashop, stock_walmart, stock_claroshop, access_token_venti)
			'''
		except Exception as e:
			_logger.info('Error en Override Save'+str(e) )
		
		rec = super(product_vqty, self).write(vals)

		return rec
