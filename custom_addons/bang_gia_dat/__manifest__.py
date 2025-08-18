{
    'name': 'Quản lý danh mục đường - Giá đất',
    'version': '1.0',
    'category': 'Land Valuation',
    'summary': 'Quản lý tên đường, đoạn đường, vị trí hành chính và giá đất',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/thua_dat_groups.xml',
        'data/dm_data.xml',
        'views/duong_views.xml',
        'views/thua_dat_views.xml',
        'views/dm_views.xml',
        'views/dm_diadanh_views.xml',
        'views/wizard_tao_doan.xml',
    ],
    'installable': True,
    'application': True,
}
