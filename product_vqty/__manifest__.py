# -*- coding: utf-8 -*-
{
    'name': "WH Producto Venti",

    'summary': """
        Webhook Producto-Venti
        """,

    'description': """
        Este módulo permite enviar una notificación a Venti para indicarle la Cantidad pronosticada
        (Forecasted) del producto al Confirmar la Orden de Venta que se recupera de Mercado Libre.
        Para todos los Mercados Electrónicos.
    """,

    'author': "APIsionate",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
}