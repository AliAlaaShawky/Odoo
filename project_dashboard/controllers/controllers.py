# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectDashboard(http.Controller):
#     @http.route('/project_dashboard/project_dashboard', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_dashboard/project_dashboard/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_dashboard.listing', {
#             'root': '/project_dashboard/project_dashboard',
#             'objects': http.request.env['project_dashboard.project_dashboard'].search([]),
#         })

#     @http.route('/project_dashboard/project_dashboard/objects/<model("project_dashboard.project_dashboard"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_dashboard.object', {
#             'object': obj
#         })

