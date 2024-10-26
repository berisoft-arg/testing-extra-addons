# Copyright 2022 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Account Payment Credit Card",
    "summary": "",
    "version": "17.0.1.0.0",
    "category": "Account",
    "author": "juanpgarza, Berisoft",
    'website': "https://berisoft.com.ar",
    "license": "AGPL-3",
    "depends": [
        "account",
        "account_payment_pro",
        ],
    "data": [
        'security/ir.model.access.csv',
        'views/account_journal_views.xml',
        'views/account_payment_views.xml',
        'views/account_payment_plan_tarjeta_views.xml',        
        ],
    "installable": True,
}
