# -*- coding: utf-8 -*-
{
    'name': 'Historico de Movimientos',
    'version' : '0.1',
    'summary': 'Registra los movimientos de inventarios',
    'description': """
        El módulo permite Revisar los historicos de inventarios de los productos.
    """,
    'category': 'Products',
    'author': 'APIsionate',
    'website': 'www.apisionate.com',
    'depends': ['base','product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/view.xml',
    ],
    'demo': [

    ],
}
