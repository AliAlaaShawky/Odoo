# -*- coding: utf-8 -*-
# from odoo import http


# class Ih-sale-product(http.Controller):
#     @http.route('/ih-sale-product/ih-sale-product', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ih-sale-product/ih-sale-product/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ih-sale-product.listing', {
#             'root': '/ih-sale-product/ih-sale-product',
#             'objects': http.request.env['ih-sale-product.ih-sale-product'].search([]),
#         })

#     @http.route('/ih-sale-product/ih-sale-product/objects/<model("ih-sale-product.ih-sale-product"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ih-sale-product.object', {
#             'object': obj
#         })

