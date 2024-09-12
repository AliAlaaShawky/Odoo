from odoo import models, fields,api

class ProjectTask(models.Model):
    _inherit = 'project.task'

    priority = fields.Selection([("0", "low"), ("1", "middle"), ("2", "high"),("3", "very high")], default='0')
    @api.model
    def get_users_for_datalist(self):
        users = self.env['res.partner'].search([])
        return users
   