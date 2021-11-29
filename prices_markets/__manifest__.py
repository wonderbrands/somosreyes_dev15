# -*- coding: utf-8 -*-
{
    'name': 'Prices Marketplaces',
    'version' : '0.1',
    'summary': 'Calcula los precios para los markets places',
    'description': """
        El módulo permite calcular los precios para los productos para cada Marketplace que 
        la empresa desea integrar.
    """,
    'category': 'Products',
    'author': 'APIsionate',
    'website': 'www.apisionate.com',
    'depends': ['base','product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/prices_view.xml',
    ],
    'demo': [

    ],
    'images': [
        'static/description/main_screen.jpg'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
