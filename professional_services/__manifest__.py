# -*- coding: utf-8 -*-
{
    'name': "Professional Services",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','contacts','sale_management','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/seq.xml',
        'views/base_menu.xml',
        'views/ticket_view.xml',
        'views/team_view.xml',
        'views/customer_view.xml',
        'views/enduser_view.xml',
        'views/order_views.xml',
        'views/tag_view.xml',
        

       
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'icon': '/professional_services/static/description/icon.png',
    'assets':{
        'web.assets_backend':{'professional_services/static/src/css/ticket.css'}

    },
    'application': True,
}

