# -*- coding: utf-8 -*-
# from odoo import http


# class SurveySimpleQuestion(http.Controller):
#     @http.route('/survey_simple_question/survey_simple_question', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/survey_simple_question/survey_simple_question/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('survey_simple_question.listing', {
#             'root': '/survey_simple_question/survey_simple_question',
#             'objects': http.request.env['survey_simple_question.survey_simple_question'].search([]),
#         })

#     @http.route('/survey_simple_question/survey_simple_question/objects/<model("survey_simple_question.survey_simple_question"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('survey_simple_question.object', {
#             'object': obj
#         })

