{
    'name': "ab_report",
    'summary': """
        Report custom""",
    'description': """
        Long description of module's purpose
    """,

    'author': "PT. Ismata Nusantara Abadi",
    'website': "https://www.ismata.co.id",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'stock', 'purchase', 'sale', 'account', 'ab_purchase_request','om_account_bank_statement_import'],
    'data': [
        'report/ab_paperformats.xml',
        'report/ab_report_actions.xml',
        'report/delivery_order_report.xml',
        'report/purchase_order_report.xml',
        # 'report/patty_cash.xml',        
        'report/patty_cash_line.xml',        
        'report/sale_order_report.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
