# -*- coding: utf-8 -*-
{
    'name': "Marketplaces Products",

    'summary': """
    Identifiacdores de Productos en los marketplaces
        
        """,

    'description': """
        Identificadores de Productos en los marketplaces
    """,

    'author': "APIsionate",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','product'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'images': [
        'static/description/icon.jpg'
    ],
}