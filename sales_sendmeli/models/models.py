# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api, _
from odoo import exceptions
from odoo.exceptions import Warning 
import json
import requests

def cuerpo_mensaje (buyer_name, tracking_number, name ):
	_logger = logging.getLogger(__name__)
	try:
		mensaje=''
		mensaje+='ESTIMADO CLIENTE: '+ buyer_name +', GRACIAS POR SU COMPRA.\n'
		mensaje+='SU PEDIDO HA SIDO REGISTRADO Y SE ENCUENTRA EN PREPARACIÓN. SU PRODUCTO SE LE ESTARÁ ENVIANDO A LA BREVEDAD\n'
		mensaje+='CON SU NÚMERO DE RASTREO / GUIA: '+str(tracking_number)+'\n'
		mensaje+='SU NUMERO DE PEDIDO INTERNO ES: '+ str(name)+'\n'
		mensaje+='FACTURA EN LINEA:'+'\n'
		mensaje+='https://somosreyes.odoo.com/portal/facturacliente/'+'\n\n'
		#mensaje+='SOLICITUD DE FACTURA: En caso de no contar con él, favor de solicitarlo a su ejecutivo de ventas.\n' 
		#mensaje+='Cuenta con 4 dias Hábiles después de recibir su Pedido para Solicitar la factura de lo contrario se factura a Público en General.\n'
		mensaje+='Cuenta hasta con el último día del mes en curso crear su factura de lo contrario se factura a Público en General.\n'
		#mensaje+='Una vez recibida la información no se podrá hacer cambios en la factura.\n '
		#mensaje+='Todos los números de Pedido comienzan con SO seguido de 5 dígitos. INGRESAR A:\n'
		#mensaje+='https://app.ventiapp.com/postventas/paso1/ye62LLN1d2go\n'
		mensaje+='IMPORTANTE Si el pedido fue realizado a través de la plataforma de MERCADO PAGO, \n\n'
		mensaje+='el método de pago siempre será 06 Dinero Electrónico.\n'
		mensaje+='EL COSTO ADMINISTRATIVO POR REFACTURACIÓN (SOLO DENTRO DEL MISMO MES CORRIENTE ) POR ERRORES AJENOS A NOSOTROS ES DE $50.00 MXN MAS IVA.\n' 
		mensaje+='Mayor información visitar nuestra pagina\n\n'
		mensaje+='www.somos-reyes.com \n'
		mensaje+='O En en los Teléfonos (55) 68309828 (55) 68309829.\n'
		return mensaje
	except Exception as e:
		_logger.info('ERROR cuerpo_mensaje(): %s ',str(e) )
		return False
		

def adjuntar_archivo(file, access_token_meli): 
	_logger = logging.getLogger(__name__)	   
	try:
		headers = {
		'Content-Type': 'multipart/form-data',
		}
		url= 'https://api.mercadolibre.com/messages/attachments?access_token='+access_token_meli

		files = {'file': open(file, 'rb')}
		
		r = requests.post(url, files = files)
		id_pdf =r.json()['id']
		_logger.info('ID PDF IN MELI: %s ',id_pdf)
		return id_pdf
	except Exception as e:
		_logger.info('ERROR adjuntar_archivo(): %s ',str(e))
		return False

def enviar_mensaje(APPLICATION_ID, access_token_meli, mensaje, id_pdf, name ):
	_logger = logging.getLogger(__name__)
	try:
		headers = {
		'content-type': 'application/json',
		}
		data={"from": {"user_id":491096624},"to":[{"user_id":491101842,"resource":"orders","resource_id":2217328156,"site_id": "MLM"}],"subject": "CONFIRMACION DE PEDIDO "+ str(name) ,"text": {"plain":mensaje}, "attachments": [str(id_pdf)],}

		url='https://api.mercadolibre.com/messages?access_token='+str(access_token_meli)+'&application_id='+str(APPLICATION_ID)
		_logger.info('URL: %s ',url)
		r=requests.post(url, data=json.dumps(data), headers=headers)
		mi_json= r.json()
		_logger.info('URL: %s ',mi_json)
	except Exception as e:
		 _logger.info('ERROR enviar_mensaje(): %s ',str(e))

def colocar_nota_a_orden_meli(so_name_reviso, order_id, access_token_meli):
	_logger = logging.getLogger(__name__)
	order_id = 2217328156 # QUITAE EN PRODUCTIVO.
	headers = {
		'content-type': 'application/json',
		} 

	data={"note":so_name_reviso}

	url='https://api.mercadolibre.com/orders/'+str(order_id)+'/notes?access_token='+access_token_meli
	try:
		r=requests.post(url, data=json.dumps(data), headers=headers)
		_logger.info('Resultado aplicar NOTA: %s ', r.text)
		return True
	except Exception as e:
		_logger.info('Error en colocar_nota_a_orden_meli(): %s ', str(e))
		return False


def get_order_meli(seller_id, order_id, access_token_meli):
	try:
		headers = {'Accept': 'application/json','content-type': 'application/json', 'x-format-new': 'true'}
		url='https://api.mercadolibre.com/orders/search?seller='+str(seller_id)+'&q='+str(order_id)+'&access_token='+access_token_meli
		r=requests.get(url, headers=headers)
		existe_order = len( r.json()['results'])

		if existe_order>0: # --- Si existe la orden
			order = r.json()['results'][0]
			shipping_id = order['shipping'].get('id')
			
			if shipping_id:	#--- Si ya tienen Orden de envio		
				return shipping_id
			else:
				return False
		else:
			return False
	except Exception as e:
		return False

def get_shipment_meli(shipping_id, access_token_meli):
	try:
		headers = {'Accept': 'application/json','content-type': 'application/json'}
		url='https://api.mercadolibre.com/shipments/'+str(shipping_id)+'?access_token='+access_token_meli

		r=requests.get(url, headers=headers)
		results = r.json()
		direccion = results['receiver_address']
		order_id=results['order_id']
		order_cost=results['order_cost']
		status = results['status']
		
		tracking_number = results.get('tracking_number')
		tracking_method = results.get('tracking_method')

		address_line = direccion['address_line']
		city = direccion['city']['name']
		country = direccion['country']['name']
		municipality = direccion['municipality']['name']
		neighborhood = direccion['neighborhood']['name']
		receiver_name = direccion['receiver_name']
		receiver_phone = direccion['receiver_phone']
		state = direccion['state']['name']
		street_name = direccion['street_name']
		street_number = direccion['street_number']
		zip_code = direccion['zip_code']

		direccion_entrega = street_name +' '+ str(street_number) +' ' + str(municipality)+  ' '+ str(neighborhood)+' '+ str(city)+' '+  str(state)+' '+str(country) +' C.P.' +str(zip_code)
		comentario = direccion['comment']
		if tracking_number:
			return dict(status=status, tracking_number=tracking_number,  tracking_method=tracking_method)
		else:
			return False

	except Exception as e:
		print (' Error get_shipment_meli: '+ str(e))
		return False


class sales_sendmeli(models.Model):
	_inherit = 'sale.order'

	#@api.multi
	def action_confirm(self):
		_logger = logging.getLogger(__name__)
		context = self._context	
		current_uid = context.get('uid')
		user = self.env['res.users'].browse(current_uid)
		_logger.info('Nombre de Usuario: %s ', user.name)

		name=self.name
		orders_id_in_odoo = self.marketplace_order_id
		pedidos= []
		if ':' in orders_id_in_odoo:#Si tiene : es un carrito con ordenes de venta
			carrito_ordenes = orders_id_in_odoo.split(':')
			carrito = carrito_ordenes[0]
			pedidos_meli = carrito_ordenes[1]
			if ',' in pedidos_meli:
				pedidos=pedidos_meli.split(',')
			else:
				pedidos.append(pedidos_meli)
		else:
			pedidos.append(orders_id_in_odoo)

		_logger.info('Pedidos: %s ', pedidos)
		#pedidos = [2217328156]

		access_token =self.access_token
		_logger.info('access_token_odoo: %s ', access_token)

		access_url=self.access_url
		_logger.info('access_url_odoo: %s ', access_url)

		seller_marketplace = self.seller_marketplace
		_logger.info('seller_marketplace: %s ', seller_marketplace ) 
		access_token_meli = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).access_token
		_logger.info('access_token_meli: %s ', access_token_meli )
		APPLICATION_ID = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).app_id
		seller_id = self.env['tokens_markets.tokens_markets'].search([['seller_name','=', seller_marketplace ]]).seller_id

		url_odoo='https://somosreyes-test-652809.dev.odoo.com'

		url = url_odoo + access_url+'?access_token='+access_token+'&report_type=pdf&download=true'
		_logger.info('URL: %s ', url )  
		myfile = requests.get(url, allow_redirects=True)

		file = '/home/odoo/pruebas/Pedido_'+str(name)+'.pdf'
		_logger.info('FILE: %s ', file )
		open(file,'wb').write(myfile.content)

		id_pdf = adjuntar_archivo(file, access_token_meli)
		_logger.info('ID MENSAJE: %s ', id_pdf)

		buyer_name = self.client_order_ref
		_logger.info('BUYER NAME: %s ', buyer_name )

		tracking_number_method = self.tracking_number

		number_method = tracking_number_method.split('/')
		tracking_method  = number_method[0]
		tracking_number = number_method[1]
		shipping_meli={'tracking_number': tracking_number ,'tracking_method':tracking_method}

		_logger.info('shipping_meli actual: %s ', shipping_meli )

		#--- recuperar y actualizar el shipment del pedido si no tiene el Tracking Number
		if tracking_method =='' or tracking_number=='':
			for order_id in pedidos:
				shipping_id = get_order_meli(seller_id, order_id, access_token_meli)
			
			if shipping_id:
				shipping_meli = get_shipment_meli(shipping_id, access_token_meli)
				_logger.info('shipping_meli: %s ', shipping_meli )
				
				tracking_number_nuevo = shipping_meli['tracking_number']
				tracking_method_nuevo = shipping_meli['tracking_method']
				#--- Actualiza el campo de tracking_number
				self.write({'tracking_number':str(tracking_method_nuevo)+'/'+str(tracking_method_nuevo)})
				self.env.cr.commit() 
				#self.tracking_number = str(tracking_method_nuevo)+'/'+str(tracking_method_nuevo)

				_logger.info('shipping_meli nuevo: %s ', shipping_meli )

		#--- Colocamos el mensaje mas el SO adjunto
		mensaje = cuerpo_mensaje (buyer_name, tracking_number, name )
		enviar_mensaje(APPLICATION_ID, access_token_meli, mensaje, id_pdf, name )

		#--- Colocamos una Nota en la Ordenes de Venta de Meli. Esta mal

		so_name_reviso = name +' - ' + user.name
		for order_id in pedidos:
			colocar_nota_a_orden_meli(so_name_reviso, order_id, access_token_meli)
			_logger.info('NOTA EN PEDIDO : %s ', order_id )

		
		rec = super(sales_sendmeli, self).action_confirm()	

		return rec
