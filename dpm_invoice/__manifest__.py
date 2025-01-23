{
    'name': 'DPM Invoice',
    'version': '17.0.1.1.0',
    'summary': '',
    'author': '',
    'category': 'Accounting',
    'depends': ['account', 'dpm_discount_amount','dpm_viewlist'],
    'data': [
        'report/dpm_invoice_report.xml',
        'views/dpm_invoice.xml',
        'report/dpm_cn_report.xml',
        'views/dpm_cn.xml',
        'report/dpm_invoice_noppn_report.xml',
        'views/dpm_invoice_noppn.xml',
    ],
    'installable': True,
    'auto_install': False,
}
