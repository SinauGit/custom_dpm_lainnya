{
    'name': 'DPM View List Enhancement',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Add additional fields in invoice list view',
    'description': """
        Add fields in invoice list view:
        - Total Quantity
        - Discount Fixed
        - Subtotal
    """,
    'depends': ['account', 'dpm_discount_amount'],
    'data': [
        'views/account_move_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
} 