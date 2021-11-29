# -*- coding: utf-8 -*-
{
    'name': "Enviar SO a Meli",

    'summary': """
        Envia la Cotización al cliente de Mercado libre al confirmarse el Presupuesto.
        """,

    'description': """
        Esta Módulo permite:

        Enviar el Pedido a Mercado Libre.

    """,

    'author': "APIsionate",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],    
}