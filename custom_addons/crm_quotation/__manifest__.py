# __manifest__.py

{
    'name': 'MHD Quotation',
    'version': '1.0',
    'author': 'Mr LNA',
    'category': 'Sales',
    'depends': ['base', 'crm'],
    'data': [
        'views/crm_lead_quotation.xml',
        'report/report.xml',
        'report/crm_quotation.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}