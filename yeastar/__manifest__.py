{
    'name': 'Call Activity Handler',
    'version': '1.0',
    'depends': ['crm', 'mail'],
    'author': 'Your Name',
    'category': 'CRM',
    'description': """
        Custom module to handle call activities in CRM, including a popup
        to ask the user whether to answer or refuse the call.
    """,
    'data': [
        #'data/yeastar_corn.xml',
         #'views/recive_call.xml',
        #'views/views.xml',
       

        
        
    ],
    'assets': {
        'web.assets_backend': [
         'yeastar/static/src/js/star.js',
         #'yeastar/static/src/js/call_handling.js',
         'yeastar/static/src/xml/star.xml'

        ],
    },
    'installable': True,
}
