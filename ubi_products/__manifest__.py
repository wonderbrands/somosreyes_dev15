# -*- coding: utf-8 -*-
{
    'name': "Ubicaciones de Productos",

    'summary': """
        Permite capturar las ubicaciones para productos Somos Reyes""",

    'description': """
         Permite capturar las ubicaciones para productos Somos Reyes
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