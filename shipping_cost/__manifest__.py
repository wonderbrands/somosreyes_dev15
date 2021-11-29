# -*- coding: utf-8 -*-
{
    'name': "Costos de Envío",

    'summary': """
        Administración de Costos de Envío de MarketsPlaces""",

    'description': """
         Administración de Costos de Envío de MarketsPlaces, permite controlar ya dministrar
         los contos de envío en que se incurre al utilizar la logistica de los diferentes canales
         de envío que se utilizan para trasportat productos a los usuarios finales.
         -Mercado Libre, acceso a su API de costeo de envío.
         -Amazon
         -Linio
         -Walmart
         -etc

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
        'views/templates.xml',
    ],
}