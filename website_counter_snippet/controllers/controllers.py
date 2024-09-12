# -*- coding: utf-8 -*-
# from odoo import http


# class WebsiteWidget(http.Controller):
#     @http.route('/website_widget/website_widget', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_widget/website_widget/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_widget.listing', {
#             'root': '/website_widget/website_widget',
#             'objects': http.request.env['website_widget.website_widget'].search([]),
#         })

#     @http.route('/website_widget/website_widget/objects/<model("website_widget.website_widget"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_widget.object', {
#             'object': obj
#         })

