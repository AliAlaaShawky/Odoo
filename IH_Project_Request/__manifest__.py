# -*- coding: utf-8 -*-
{
    'name': "IH_Project_Request",

    'summary': "Create a Task Request From Portal User",

    'description': """
Create a Task Request From Portal User , Each customer has portal access , can create request from portal and select the Subscription
    """,

    'author': "My Company",
    'website': "https://www.inspirehub.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Project',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['project', 'portal','website','sale_management','timesheet_grid'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/allow_view_contatcs.xml',
        'views/views.xml',
        'views/templates.xml',
        #'views/order.xml',

    ],
    'assets': {
        'web.assets_frontend': [
            'IH_Project_Request/static/src/js/star.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

