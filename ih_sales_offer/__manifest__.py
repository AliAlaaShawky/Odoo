# -*- coding: utf-8 -*-
{
    'name': "IH_sales_offer",

    'summary': "Add new sales offer",

    'description': """
Long description of module's purpose
    """,

    'author': "Inspire Hub",
    'website': "https://www.inspirehub.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['sale','purchase','stock','web_studio'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/price.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
     'assets': {
        'web.assets_backend': [
            #'ih_sales_offer/static/src/js/product_pricelist.js',
          
        ],
    },
}

