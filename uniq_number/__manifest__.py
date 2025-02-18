{
    'name': "Customer Sequence",
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': """Customer code for Customers""",
    'description': """Each customer has a unique customer code when creating.""",
    'depends': ['sale','sale_management', 'account', 'purchase'],
    'data': [
        'views/res_company_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'auto_install ': False,
    'application': False
}
