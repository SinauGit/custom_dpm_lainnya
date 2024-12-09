{
    'name': "Custom Purchase Aggrement",

    'summary': """
        Modul yang mengcustom fitur default purchase aggrement""",

    'description': """
        Menambahkan menu purchase request dan purchase tender beserta fitur-fitur pendukungnya
    """,

    'author': "PT. Ismata Nusantara Abadi",
    'website': "https://ismata.co.id",
    'category': 'Inventory/Purchase',
    'version': '0.1',
    'depends': ['base', 'purchase', 'purchase_requisition'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'data/default_data.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/sequence_views.xml'
    # ],
    # 'demo': [
    #     'demo/demo.xml',
    ],
    'application': True
}
