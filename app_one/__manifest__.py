# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'UC APP',
    'version' : '1.41',
    'summary': 'Sales and orders',
    
    

    'depends': ['base',
    ],

    'data': [
        'security/ir.model.access.csv',
        
        'views/base_menu.xml',
        'views/property_view.xml',
      
    ],
    
 
    'application': True,
    
}
