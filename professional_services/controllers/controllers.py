# -*- coding: utf-8 -*-
# from odoo import http


# class ProfessionalServices(http.Controller):
#     @http.route('/professional_services/professional_services', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/professional_services/professional_services/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('professional_services.listing', {
#             'root': '/professional_services/professional_services',
#             'objects': http.request.env['professional_services.professional_services'].search([]),
#         })

#     @http.route('/professional_services/professional_services/objects/<model("professional_services.professional_services"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('professional_services.object', {
#             'object': obj
#         })

