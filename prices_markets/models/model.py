# -*- coding: utf-8 -*-
import logging
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from odoo.exceptions import UserError
from odoo.tools.translate import _

import json
import requests

def update_product_venti(json_venti, access_token_venti):
    try:
        _logger = logging.getLogger(__name__)
        headers={"content-type":"application/json","Authorization":"bearer "+ access_token_venti}
        body=json_venti

        url='https://ventiapi.azurewebsites.net/api/stock/updatepricestockbychannel'

        r=requests.post(url, headers=headers, data=body)

        _logger.info('VENTI REQUESTS HEADERS: %s ', str(r.request.headers) )
        _logger.info('VENTI REQUESTS BODY: %s ', str(r.request.body) )
        _logger.info('VENTI RESPONSE: %s ', str(r.text) )    

        if "Producto no encontrado" in r.text:
            _logger.info(r.text)

        if "Authorization has been denied for this request" in r.text:
            _logger.info('ERROR VENTI|Actualizando SKU: '+str(r.text))
        else:
            _logger.info('INFO|Actualizando SKU: '+str(json_venti))
        return True

    except Exception as e:
        _logger.info('ERROR|update_product_venti|'+ str (e))
        return False

def get_shipping_cost(zip_code_from, zip_code_to, ancho, largo, alto, precio ):
    try:
        _logger = logging.getLogger(__name__)

        headers = {'Accept': 'application/json','content-type': 'application/json'}
        dimensiones=str(ancho)+'x'+str(largo)+'x'+str(alto)
        url = 'https://api.mercadolibre.com/sites/MLM/shipping_options?zip_code_from='+str(zip_code_from)+'&zip_code_to='+str(zip_code_to)+'&dimensions='+dimensiones+','+str(precio)
        _logger.info('URL: %s ', str(url) )

        r=requests.get(url, headers=headers)
        #print (json.dumps(r.json()['options'], indent=4, sort_keys=True))
        options=json.dumps(r.json()['options'])
        lista_costos =[]
        for option in json.loads(options):
            #name = option['name'], 
            cost = option['cost']
            lista_costos.append(cost)

        costo_maximo = max(lista_costos)
        costo_minimo = min(lista_costos)
        _logger.info('Costo Envio Maximo: %s, Costo Envio Minimo: %s  ', costo_maximo, costo_minimo)

        costo_promedio= round( (float(costo_maximo)+float(costo_minimo) )/2,2)
        
        return costo_promedio
    except Exception as e:
        _logger.error('get_shipping_cost(): %s ', str(e))
        return False

class PriceTemplate(models.Model):
    _inherit = "product.template"
    sub_price_line_ids = fields.One2many('sub.price.lines', 'price_tmpl_ref_id', string='Precios')

class SubPriceLines(models.Model):
    _name = "sub.price.lines"

    price_tmpl_ref_id = fields.Many2one('product.template', string='Referencia de precios')
    name_marketplace = fields.Selection([('mercado_libre', 'Mercado Libre'), ('amazon', 'Amazon'),('linio', 'Linio'), ('walmart','Walmart'),('claroshop','ClaroShop'),('elektra','Elektra'),('liverpool','Liverpool'),('somos_reyes_shop','Somos Reyes Shop')],'Marketplace')
    fee_marketplace = fields.Float('Comisión %', compute='_calcula_min_price_to_post',  store=True)
    extra_marketplace = fields.Float('Comisión Extra $')
    shipping_price = fields.Float('Costo de Envío')
    discount_shipping_price = fields.Float('Descuento Envío %')

    min_price_to_post = fields.Float('Costo Mínimo', compute='_calcula_min_price_to_post',  store=True)
    margen_ganancia = fields.Float('Margen ganancia %')   
    min_suggested_price = fields.Float('Precio Sugerido', compute='_calcula_min_price_to_post', store=True)
    recommended_price = fields.Float('Precio Recomendado')
    competition_price = fields.Float('Precio competencia')
    marketplace_price = fields.Float('Precio Marketplace', compute='_calcula_min_price_to_post',  store=True)

    #@api.one
    @api.depends('name_marketplace','fee_marketplace' ,'extra_marketplace','recommended_price','margen_ganancia','shipping_price')
    #@api.onchange('marketplace_order_id')
    def _calcula_min_price_to_post(self):
        _logger = logging.getLogger(__name__)

        # caluslando el precio con IVA
        precio_iva = round( self.price_tmpl_ref_id.list_price * 1.16,2)
        
        costo_producto = float(self.price_tmpl_ref_id.standard_price)  
        #recommended_price_actual= self.recommended_price

        if self.name_marketplace:
            _logger.info('Stantard Price: %s ', self.price_tmpl_ref_id.standard_price)
            _logger.info('Name Marketplace: %s', self.name_marketplace)
            
            categoria = self.env['product.template'].search_read([('default_code', '=', self.price_tmpl_ref_id.default_code)] )
            #_logger.info('Categoria: %s ', str(categoria) ) # Muestras todos los datos del Producto.

            categoria_id = categoria[0]['categoria_id'][0] # Extrae de aqui--> ej:'categoria_id': (83, 'Juegos y Juguetes')
            _logger.info('Categoria Id: %s ', str(categoria_id) )

            categoria_markets = self.env['categorias_productos'].search_read([('id', '=', categoria_id)])

            #_logger.info('Categoria Marketplace: %s ', str(categoria_markets) )

            volumen = float(self.env['product.template'].search([('default_code', '=', self.price_tmpl_ref_id.default_code)]).volumen)
            #--- Politica de costo de envío para los productos de Somos Reyes:
            #    1. Si el MarketPlace es Mercado Libre, el costo de envío se obtiene del campo: Costo de Envio del Modulo de Categorias de Somos  Reyes.
            #    2. Si el Marketplace es diferente a Mercado Libre el Costo se Obtendra del Modulo : Costos de Envio, dependiendo de su Volumetrico. 
            
            costo_envio_market = self.env['shipping_cost'].search([('name_marketplace', '=', self.name_marketplace),('peso_volumetrico_inferior','<',volumen)] )
            _logger.info('costo_envio_market: %s ', str(costo_envio_market) )
            resultados = len(costo_envio_market)

            if str(self.name_marketplace) == 'mercado_libre':
                self.fee_marketplace = float(categoria_markets[0]['comision_mercado_libre'])

            elif str(self.name_marketplace) == 'amazon':
                self.fee_marketplace = float(categoria_markets[0]['comision_amazon'])
                resultados = 1

            elif str(self.name_marketplace) == 'linio':
                self.fee_marketplace = float(categoria_markets[0]['comision_linio'])
                resultados = 1

            elif str(self.name_marketplace) == 'walmart':
                self.fee_marketplace = float(categoria_markets[0]['comision_walmart'])

            elif str(self.name_marketplace) == 'claroshop':
                self.fee_marketplace = float(categoria_markets[0]['comision_claroshop'])

            elif str(self.name_marketplace) == 'elektra':
                self.fee_marketplace = float(categoria_markets[0]['comision_elektra'])
                resultados = 1

            elif str(self.name_marketplace) == 'liverpool':
                self.fee_marketplace = float(categoria_markets[0]['comision_liverpool'])

            elif str(self.name_marketplace) == 'somos_reyes_shop':
                self.fee_marketplace = float(categoria_markets[0]['comision_somos_reyes'])
                resultados = 1

            _logger.info('Fee markeplace: %s ', self.fee_marketplace)
            
            costo_envio = 0.0
            if resultados:

                if str(self.name_marketplace) == 'mercado_libre':
                    costo_envio = float(categoria_markets[0]['costo_envio_meli'])
                    _logger.info('MERCADO LIBRE costo_envio_meli: %s ', costo_envio)

                elif str(self.name_marketplace) == 'amazon':
                    costo_envio = float(self.shipping_price)
                    _logger.info('AMAZON shipping_price: %s ', costo_envio)
                
                elif str(self.name_marketplace) == 'linio':
                    costo_envio = float(self.shipping_price)
                    _logger.info('LINIO shipping_price: %s ', costo_envio)
                
                elif str(self.name_marketplace) == 'somos_reyes_shop':
                    costo_envio = float(self.shipping_price)
                    _logger.info('LINIO shipping_price: %s ', costo_envio)
                
                elif str(self.name_marketplace) == 'elektra':
                    costo_envio = float(self.shipping_price)
                    _logger.info('ELEKTRA shipping_price: %s ', costo_envio)

                else:
                    costo_envio = costo_envio_market[resultados-1].shipping_price  - ((costo_envio_market[resultados-1].shipping_price )*(self.discount_shipping_price/100) )

                # Para todo Marketplace el costo de envío menor a 499 corre a cargo del cliente, por lo tanto no lo tomamos como parte
                # de nuestra politica de Costos.
                if precio_iva < 499.0 :
                    costo_envio = 0.0

                _logger.info('Volumen: %s,  costo_envio_market: %s ', volumen,  costo_envio)
                self.shipping_price =costo_envio

                self.min_price_to_post = round( ( ((costo_producto*1.16) * (1.0+(self.fee_marketplace/100))) + costo_envio)+ self.extra_marketplace ,2)  
                # -Minimo precio sugerido+ margen ganancia
                self.min_suggested_price = round(self.min_price_to_post * (1+(self.margen_ganancia/100) ), 2)

                if self.recommended_price > self.min_price_to_post:
                    self.marketplace_price = self.recommended_price

                if self.recommended_price <= self.min_suggested_price:
                    self.margen_ganancia = categoria_markets[0]['margen_ganancia_minima']
                    recommended_price_calculated = self.min_suggested_price * ( 1 + (categoria_markets[0]['margen_ganancia_minima']/100.0) )
                    #recommended_price_calculated = self.min_suggested_price * 1.10
                    self.recommended_price = recommended_price_calculated
            
    #@api.one
    #@api.depends('name_marketplace')
    def _costo_envio(self):
        zip_code_from = '53460'
        zip_code_to = '22504'

        ancho =int(self.price_tmpl_ref_id.ancho)
        largo = int(self.price_tmpl_ref_id.largo)
        alto = int(self.price_tmpl_ref_id.alto)
        precio = int(self.price_tmpl_ref_id.precio_con_iva)

        costo_envio = get_shipping_cost(zip_code_from, zip_code_to, ancho, largo, alto, precio)

        self.shipping_price = round(costo_envio, 2)

class product_precios(models.Model):
    _inherit = 'product.template'
    #mlms = fields.Char(string="MLM MeLi")

    #@api.multi
    def actualizar_precio_venti(self):
        _logger = logging.getLogger(__name__)
        try:
            seller_name = 'VENTI-SOMOSREYES'
            access_token_venti = str(self.env['tokens_markets.tokens_markets'].search([('seller_name', '=', seller_name)]).access_token )

            default_code =self.default_code
            prices = self.sub_price_line_ids
            _logger.info('sub_price_line_ids: %s ', self.sub_price_line_ids)

            json = ''
            for line in prices:
                _logger.info(' Sku: %s,  Marketplace: %s, Fee: %s, Price: %s',default_code, line.name_marketplace, line.fee_marketplace, line.marketplace_price)

                if line.name_marketplace == 'mercado_libre':
                    price_mercadolibre = line.marketplace_price
                    json += '{"channel":"mercadolibre","price":'+ str(int(price_mercadolibre))+'},'

                if line.name_marketplace == 'amazon':
                    price_amazon = line.marketplace_price
                    json += '{"channel":"amazon","price":'+str(int(price_amazon))+'},'

                if line.name_marketplace == 'linio':
                    price_linio = line.marketplace_price
                    json += '{"channel":"linio","price":'+str(int(price_linio)) +'}'

                if line.name_marketplace == 'walmart':
                    price_walmart = line.marketplace_price
                    json += '{"channel":"walmart","price":'+ str(int(price_walmart))+'},'

                if line.name_marketplace == 'claroshop':
                    price_claroshop = line.marketplace_price
                    json += '{"channel":"claroshop","price":'+ str(int(price_claroshop))+'},'

                if line.name_marketplace == 'elektra':
                    price_elektra = line.marketplace_price
                    json += '{"channel":"elektra","price":'+str( int(price_elektra))+'},'

                if line.name_marketplace == 'liverpool':
                    price_liverpool = line.marketplace_price
                    json += '{"channel":"liverpool","price":'+ str(int(price_liverpool))+'},'

                if line.name_marketplace == 'somos_reyes_shop':
                    price_prestashop = line.marketplace_price
                    json += '{"channel":"prestashop","price":'+str(int(price_prestashop))+'},'

            if json !='':
                json_venti = '{"sku":"'+ str(default_code+'"' )+', "channelData": ['+json+']}'
                _logger.info('VENTI JSON: %s ', json_venti)
                update_product_venti(json_venti, access_token_venti)
            else: 
                _logger.info('NO VENTI JSON')

        except Exception as e:
            msg_error = _('Error en actualizar_precio_venti(): %s') % (e)
            _logger.Error ('Error en actualizar_precio_venti(): %s', e)
            raise UserError(msg_error)



