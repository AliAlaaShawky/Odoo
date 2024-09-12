
{
    'name': 'Custom Snippet',
    'version': '1.0',
    'summary': 'Custom Snippets for Odoo 17',
    'description': 'A module that adds custom snippets to Odoo 17.',
    'category': 'Website',
    'depends': ['website'],
    'data': [
        'views/counter_snippet_template.xml',
        'views/snippet_inclusion.xml',
        
    ],
     'assets': {
        'web.assets_frontend': [
            'website_counter_snippet/static/src/js/counter.js',
            'website_counter_snippet/static/src/css/counter.css',
        ],
       
    },
    
}
