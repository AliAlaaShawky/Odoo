# -*- coding: utf-8 -*-
# __manifest__.py
{
    'name': 'My Custom Survey',
    'version': '1.0',
    'category': 'Survey',
    'summary': 'Custom Survey Template',
    'description': """A custom survey template with simplified styling.""",

    'author': "Inspire Hub",
    'website': "https://www.inspirehub.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    # any module necessary for this one to work correctly
    'depends': ['survey'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
         'views/survey.xml',
    ],
    
    'assets':{
        'survey.survey_assets':['survey_simple_question/static/src/scss/survey_styles.scss']

    },

    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

