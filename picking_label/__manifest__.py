# -*- coding: utf-8 -*-
{
    'name': "picking_label",

    'summary': """
        Impresión del Reporte de Picking con Códigos de Barras""",

    'description': """
        -Este módulo permite la impresión del reporte de Picking con Codigos de Barras
        -Agrega los campos de Se imprimio la Etiqueta de Meli, referencia_entrega, Dirección de etrega,
        comentarios, Impresión de Salida con Codigo de Barras, Última ubicación de producto.

    """,

    'author': "APIsionate",
    'website': "http://APIsionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','sale','product','pre_picking'],

    # always loaded
    'data': [
        #'security/security.xml',
        #'security/ir.model.access.csv',
        #'security/security_rules.xml',
        'views/picking_label_view.xml',
        'views/picking_package.xml',
        'views/templates.xml',
        'views/picking_label_report.xml',
        'report/picking_label_list_reports_views.xml',
        'report/picking_label_list_report.xml',

    ],

    'images': [
        'static/description/icon.jpg'
    ],    
}