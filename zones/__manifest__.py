# -*- coding: utf-8 -*-
{
    'name': "Zonas de Picking",

    'summary': """
        Permite capturar las Zonas de Picking de Somos Reyes""",

    'description': """
        Permite capturar las Zonas de Picking de Somos Reyes
    """,

    'author': "APIsionate",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],

}