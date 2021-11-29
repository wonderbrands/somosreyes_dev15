# -*- coding: utf-8 -*-
{
    'name': "Importation Fields",

    'summary': """
        Adiciona campos para la importación-exportación comercial de productos.
        """,

    'description': """
        Este módulo Adiciona campos para la importación exportación comercial de productos.

    """,

    'author': "Moises Rodrigo Santiago Garcia",
    'website': "http://www.APIsionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/import_product_view.xml',
    ],

}