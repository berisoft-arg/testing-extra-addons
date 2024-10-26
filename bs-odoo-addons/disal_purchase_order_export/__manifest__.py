{
    'name': 'Disal Purchase Order XLSX Export',
    'version': '17.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Exporta la orden de compra a xlsx para importarla a la web de Disal',
    'author': "Berisoft",
    'website': "https://berisoft.com.ar",
    'depends': ['purchase', 'report_xlsx'],
    'data': ['report/purchase_order_xlsx.xml','report/ir_actions_report.xml',
        'report/purchase_order_view.xml',],
    'installable': True,
}
