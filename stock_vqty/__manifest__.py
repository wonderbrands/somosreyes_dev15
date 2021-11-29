# -*- coding: utf-8 -*-
{
    'name': "Stock Webhook",

    'summary': """
        Modulo que permite enviar auna notificación a Venti y actualizar los Stocks""",

    'description': """
        Este módulo permite enviar una notificación en cada validación de algun movimiento
        inter alamacenes.
        Si el movimiento es un WH/INT y no se tiene documento Origen (SO ó PO) 
        se debe avisar a Venti la existencia de AG/Stock de ese producto

    """,

    'author': "APIsionate",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    
}