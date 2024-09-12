# -*- coding: utf-8 -*-
{
    'name': "project_dashboard",

    'summary': "project dashboard ",

    'description': """
project dashboard
    """,

    'author': "Ali Alaa",
    'website': "https://www.inspirehub.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'project',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','project','sale_management','sale_timesheet',],

    # always loaded
    'data': [
       'views/views.xml',

        
    ],
    # only loaded in demonstration mode
    'assets': {
            'web.assets_backend': [
                 
                'project_dashboard/static/src/css/dashboard.css',
               
                'project_dashboard/static/src/js/dashboard.js',
               'project_dashboard/static/src/xml/dashboard.xml',
                



            ]


    },
}

