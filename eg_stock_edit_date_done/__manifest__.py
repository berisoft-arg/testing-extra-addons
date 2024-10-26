{
    'name': 'Stock Picking Edit Done Date',
    'version': '17.0',
    'category': 'stock',
    'summery': 'Stock Picking Edit Done Date',
    'author': 'INKERP',
    'website': "http://www.inkerp.com",
    'depends': ['stock'],
    
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/stock_picking_view.xml',
        'wizards/update_effective_date_view.xml',
    ],
    
    'images': ['static/description/banner.png'],
    'license': "OPL-1",
    'installable': True,
    'application': True,
    'auto_install': False,
}
