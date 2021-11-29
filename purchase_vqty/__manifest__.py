# -*- coding: utf-8 -*-
{
    'name': "WH Purchase",

    'summary': """
    Webhook Purchase Order.
    Módulo que permite notificar a Venti cuando se realiza una compra de productos
    y se incrementa el stock en Odoo (Entrada de productos). 
    """,
    
    'description': """
       Este Módulo notifica a la API de Venti, cuando se realiza una Orden de Compra
       (Purchase Order) PO en Odoo. Se toma el SKU del producto y de actualiza al 
       endpoit multicanal de Venti :

       https://ventiapi.azurewebsites.net/api/stock/updatepricestockbychannel

       El cual actualiza el stock en Venti para los Marketplaces:

       -Mercado Libre
       -Linio
       -Amazon
       -Walmart
       -Prestshop
       -Claroshop

       El stock de cada producto esta descrito en el Excel de Politcas de Stock
       de Somos-Reyes.

    """,

    'author': "APIsionate",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}