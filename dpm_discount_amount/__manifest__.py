{
    "name": "DPM Discount Amount",
    "version": "17.0.1.1.0",
    "summary": "Diskon dengan nominal tetap pada Sales Order dan Invoice",
    "category": "Sales/Sales",
    "author": "PT. Digital Prima Sejahtera",
    "website": "https://dpm.id",
    "depends": [
        "base",
        "sale",
        "account"
    ],
    "data": [
        "security/res_groups.xml",
        "security/ir.model.access.csv",
        "views/sale_order_views.xml",
        "views/account_move_view.xml",
        "reports/report_sale_order.xml",
        "reports/report_account_invoice.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
    "application": False,
    "auto_install": False,
}
