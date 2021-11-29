## -*- coding: utf-8 -*-
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
		_logger.info('STOCK SKU: %s Meli %s |  Linio %s |Amazon %s |Prestashop %s |Walmart %s |ClaroShop %s en Venti.', sku, str(stock_mercadolibre), str(stock_linio), str(stock_amazon), str(stock_prestashop), str(stock_walmart), str(stock_claroshop) )
		_logger.info('STOCK Respuesta Venti| %s ', r.text )  

	except Exception as e:
		_logger.error('Error en stock_vqty|update_product_venti()|%s', str (e))


class stock_vqty(models.Model):
	_inherit = 'stock.picking'

	@api.multi
	def button_validate(self):
		_logger = logging.getLogger(__name__)
		# Si el movimiento es un WH/INT y no se tiene documento Origen (SO ó PO) 
		# se debe avisar a Venti la existencia de AG/Stock de ese producto
		# 1. Primero saber si el movimiento es un traspaso interno (WH/INT)
		name = self.name
		_logger.info('Nombre del Movimiento %s', name)
		if 'INT' in name:
			_logger.info('Movimiento interno de producto')

			# 2. Obtener los ids de los Productos que se estan moviendo en ese traspaso entre almacenes.
			lines =self.move_lines.ids

			_logger.info('Lines:' + str(lines) )

			lines = len(self.move_lines.ids)

			#--- Obtenemos el Token de ese Seller Id
			access_token_venti = self.env['tokens_markets.tokens_markets'].search([['name_marketplace','=', 'VENTI' ]]).access_token

			ids_product=[]
			vqty_product=[]
			skus_product =[]
			products_stock_real=[]
			x=0
			for x in range(lines):
				#--- Recuperados el Id del Producto en Odoo
				ids_product.append(self.move_lines[x].product_id.id)
				id_product = self.move_lines[x].product_id.id
				stock_real = self.move_lines[x].product_id.stock_real
				_logger.info('stock_real recuperado1:%s',str(stock_real) )

				_logger.info('Procesando:' + str(id_product) )

				#--- Recuperamos el Sku de cada producto en Odoo
				sku = self.env['product.product'].search([['id', '=', id_product ]]).default_code
				default_code = self.env['product.product'].search([['id', '=', id_product ]]).default_code
				skus_product.append(default_code)

				#--- Recuperamos la Cantidad Pronosticada
				virtual_available = self.env['product.product'].search([['id', '=', id_product ]]).virtual_available
				vqty_product.append(virtual_available)
				_logger.info('virtual_available:%s',str(virtual_available) )

				#--- Recuperamos el Stock Real que tiene Somos Reyes
				
				products_stock_real.append(stock_real)
				#--- Recuperamos el stock de exclusivas
				stock_exclusivas = self.env['product.product'].search([['id', '=', id_product ]]).stock_exclusivas
				#--- Recuperamos el stock de Urrea
				stock_urrea = self.env['product.product'].search([['id', '=', id_product ]]).stock_urrea			
				#--- Recuperamos el stock de Markets
				stock_markets_actual = self.env['product.product'].search([['id', '=', id_product ]]).stock_markets

				#--- Recuperamos la cantidad que se hace de este producto en el pedido actual (self)
				product_uom_qty = self.move_lines[x].product_uom_qty
				location_dest_id = self.move_lines[x].location_dest_id

				stock_real = self.env['product.product'].search([['id', '=', id_product ]]).stock_real
				stock_real=stock_real+product_uom_qty
				_logger.info('stock_real recuperado:%s',str(stock_real) )
				
				#location_dest_id.name = self.move_lines[x].location_dest_id.name
				location_dest_id_name = location_dest_id.name
				_logger.info('Nombre Destino:%s',str(location_dest_id_name) )
				
				#--- calculamos el nuevo stock para actualizar en meli, para cada marketplace. 
				stock_markets_nuevo = stock_real + stock_exclusivas + stock_urrea - product_uom_qty

				#---Calculamos politicas de stock para cada marketplace
				stock_mercadolibre =  stock_real + stock_exclusivas + stock_urrea - product_uom_qty
				stock_linio = stock_real + stock_exclusivas   - product_uom_qty
				stock_amazon = stock_real + stock_exclusivas + stock_urrea  - product_uom_qty
				stock_prestashop = stock_real + stock_exclusivas + stock_urrea  - product_uom_qty
				stock_walmart = stock_real + stock_exclusivas   - product_uom_qty
				stock_claroshop = stock_real + stock_exclusivas+ stock_urrea  - product_uom_qty
			
				_logger.info('STOCK | Id: %s | SKU:  %s | stock_real: %s | product_uom_qty:%s |stock_markets_nuevo : %s', str(id_product), str(sku) , str(stock_real),str(product_uom_qty),str(stock_markets_nuevo) )
				_logger.info('STOCK Meli: %s| Linio: %s | Amazon:  %s | Prestashop: %s |Walmart : %s |Claroshop: %s ',str(stock_mercadolibre), str(stock_linio), str(stock_amazon), str(stock_prestashop), str(stock_walmart), str(stock_claroshop))
				
				#update_product_venti(sku, stock_mercadolibre, stock_linio, stock_amazon, stock_prestashop, stock_walmart, stock_claroshop, access_token_venti)
				#---Actualizamos el campo stock_markets del Producto

				producto = self.env['product.product'].search([('id', '=',id_product )])
				producto.write({'stock_markets': stock_markets_nuevo})
		
		elif 'PICK' in name:
			_logger.info('Se ha realizado el PICK de producto')
			#---Obtenemos el Id del Pre piccking que coincide con el SO origen
			pre_picking_id = self.env['pre_picking'].search([['name','=', self.origin ]])
			#---Marcamos el Pre Picking como Procesado
			pre_picking_id.write({'estado':'en_proceso'})
			self.env.cr.commit() 

		else:
			_logger.info('Movimiento  No interno de producto')
						
		rec = super(stock_vqty, self).button_validate()	

		return rec
