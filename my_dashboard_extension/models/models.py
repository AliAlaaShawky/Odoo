# my_custom_module/models/sale_order.py

from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
