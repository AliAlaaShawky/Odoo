# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class survey_simple_question(models.Model):
#     _name = 'survey_simple_question.survey_simple_question'
#     _description = 'survey_simple_question.survey_simple_question'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

