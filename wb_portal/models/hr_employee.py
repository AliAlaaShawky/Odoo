# # # my_module/models/hr_employee.py
# from odoo import models, fields, api

from odoo import models, fields, api

# # my_module/models/hr_employee.py
class ResPartner(models.Model):
    _inherit = 'res.partner'

    employee_id = fields.Many2one('hr.employee', string='Related Employee')

    @api.model
    def create(self, vals):
        contact = super(ResPartner, self).create(vals)
        if 'name' in vals and 'email' in vals:
            employee = self.env['hr.employee'].search([
                ('name', '=', vals['name']),
                ('work_email', '=', vals['email'])
            ], limit=1)
            if employee:
                contact.employee_id = employee.id
        return contact
# models/hr_leave.py (or appropriate model file)
               

# In your view, you can display the approver_table field using the `widget="html"` option to render the HTML content.

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    def action_approve(self):
        for record in self:
            record.write({'state': 'validate1'})

    def action_refuse(self):
        for record in self:
            record.write({'state': 'refuse'})
# approval_request = env['approval.request'].create({
#     'name': record.name,  # Use the name of the created purchase order
#     'request_owner_id': env.user.id,
#     'category_id': 10,  # Replace with your approval category ID
#     'reason': 'This is an automated approval request.',
# })

# # Update the purchase order with the created approval request ID
# record.write({'approval_request_id': approval_request.id})
