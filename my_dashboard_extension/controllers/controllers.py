# -*- coding: utf-8 -*-
# from odoo import http


# class MyDashboardExtension(http.Controller):
#     @http.route('/my_dashboard_extension/my_dashboard_extension', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_dashboard_extension/my_dashboard_extension/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_dashboard_extension.listing', {
#             'root': '/my_dashboard_extension/my_dashboard_extension',
#             'objects': http.request.env['my_dashboard_extension.my_dashboard_extension'].search([]),
#         })

#     @http.route('/my_dashboard_extension/my_dashboard_extension/objects/<model("my_dashboard_extension.my_dashboard_extension"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_dashboard_extension.object', {
#             'object': obj
#         })

