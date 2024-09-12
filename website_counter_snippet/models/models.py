# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class website_widget(models.Model):
#     _name = 'website_widget.website_widget'
#     _description = 'website_widget.website_widget'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields, api

class WebsiteCounterSnippet(models.Model):
    _inherit = 'website'

    @api.model
    def get_counter_data(self):
        # Your logic here
        return {'target': 1000}
