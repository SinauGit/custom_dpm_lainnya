{
    'name': 'DPM Invoice Report',
    "version": "17.0.1.1.0",    
    'summary': '',
    'author': '',
    'category': 'Report',
    'depends': ['account'],
    'data': [
        'report/dpm_invoice_report.xml',
        'views/dpm_invoice.xml',
        'report/dpm_cn_report.xml',
        'views/dpm_cn.xml',
        'report/dpm_invoice_noppn_report.xml',
        'views/dpm_invoice_noppn.xml',
    ],
    'installable': True,
    'application': False,
}
