# -*- coding: utf-8 -*-
{
    'name': "sales_vqty",

    'summary': """
        Webhook al Confirmar la Orden de Ventas (Sales Order), de odoo.
        """,

    'description': """
        Esta Módulo permite:

        1. Calcular la cantidad de piezas disponibles para los mercados electrónicos.
        2. Recalcular y notificar a Odoo la nueva existencia.
        Al presionar el botón Confirmar de la Orden de Venta, se actualiza la Existencia
        en el campo Stock Market de la siguiente manera:
        Stock Exclusivas+Stock Urrea + Pronosticado - Piezas pedidas en la Orden de Venta.
        3. Se actualiza la nueva existencia en el campo Stock Mercados
        4. Se envia  la nueva existencia a la API de Venti (Existencias multicanal)

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