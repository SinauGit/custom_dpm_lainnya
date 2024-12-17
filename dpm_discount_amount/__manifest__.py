{
    "name": "DPM Discount Amount",
    "version": "17.0.1.1.0",
    "summary": "Fixed nominal discount on Sales Order and Invoice",
    "category": "Sales/Sales",
    "author": "",
    "website": "",
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
