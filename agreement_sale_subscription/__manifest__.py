# Copyright (C) 2019 - TODAY, Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Agreement - Sales Subscription',
    'summary': 'Link your sales subscriptions to an agreement',
    'version': '12.0.1.0.1',
    'license': 'LGPL-3',
    'author': 'Open Source Integrators',
    'category': 'Agreement',
    'website': 'https://github.com/ursais/osi-addons',
    'depends': [
        'agreement_legal_sale',
        'sale_subscription'
    ],
    'data': [
        'views/agreement.xml',
        'views/subscription.xml'
    ],
    'installable': True,
}
