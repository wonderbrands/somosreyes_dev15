## -*- coding: utf-8 -*-
{
    'name': "Automatización de Entregas",

    'summary': """
        Automatiza el proceso de Picking desde el Presupuesto.
        """,

    'description': """
    Automatiza el proceso de Picking desde el Presupuesto,permitiendo imprimir la Salida del con Código de Barras
    desde el presupuesto mismo e inmediatamente procesar el Pick del Presupuesto confirmado (Orden de venta) sin 
    tener que salir de la ventana de la Orden de Venta.
        
        Esta Módulo permite:

        Desde el pedido de Ventas SO hacer que cuando se presion Confirmar el sistema :
            -Imprime el albarán de Salida (Pick)
            -Marque que se ha impreso la Etiqueta en el CheckBox
            -Muestre la Disponibilidad de Producto a entegar.
            -Aparte la cantidad de producto pedida y marque el cambio en el Picking.

    """,

    'author': "APIsionate",
    'website': "http://www.apisionate.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/report.xml', # reporte personalizado con codigo de barras llamada desde el boton Imprimir Salida.

    ],
    'images': [
        'static/description/icon.jpg'
    ],    
}