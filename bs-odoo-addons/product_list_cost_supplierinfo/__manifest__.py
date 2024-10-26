# -*- coding: utf-8 -*-
{
    'name': "Product List Cost Supplierinfo",

    'summary': """
        Agrega nombre de Lista de Precio en Tarifa Proveedor""",

    'description': """
        Este modulo agrega una columna para indicar el nombre de Lista de Precio en 
        Tarifa Proveedor, y hace el calculo de costo final.
    """,

    'author': "Berisoft",
    'website': "https://berisoft.com.ar",    
    'category': 'Purchase',
    'version': '17.0.1.0.0',
    'depends': ['product'],
    
    'data': [
        'views/product_supplierinfo_views.xml',
    ],

    'installable': True,
        
}
