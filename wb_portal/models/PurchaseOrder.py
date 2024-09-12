# # # # my_module/models/hr_employee.py
# # from odoo import models, fields, api

from odoo import models, fields, api


# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
    
#     approval_request_id = fields.Many2one('approval.request', string='Approval Request')
#     approver_names = fields.Char(string='Approver Names', compute='_compute_approver_name')
#     approvers_details = fields.One2many('purchase.order.approver.detail', 'purchase_order_id', string='Approvers Details', compute='_compute_approver_details')

#     @api.depends('approval_request_id')
#     def _compute_approver_name(self):
#         for record in self:
#             approvers_info = self._get_approvers_info(record)
#             if approvers_info:
#                 approver_names_list = [f"{approver['name']} ({approver['status']})" for approver in approvers_info]
#                 record.approver_names = ", ".join(approver_names_list)
#             else:
#                 record.approver_names = False

#     @api.depends('approval_request_id')
#     def _compute_approver_details(self):
#         ApproverDetail = self.env['purchase.order.approver.detail']
#         for record in self:
#             record.approvers_details.unlink()
#             approvers_info = self._get_approvers_info(record)
#             if approvers_info:
#                 for approver in approvers_info:
#                     ApproverDetail.create({
#                         'purchase_order_id': record.id,
#                         'name': approver['name'],
#                         'status': approver['status']
#                     })

#     def _get_approvers_info(self, record):
#         if record.approval_request_id and record.approval_request_id.approver_ids:
#             approvers_info = []
#             for approver in record.approval_request_id.approver_ids:
#                 name = approver.user_id.name
#                 status = approver.status  # Assuming `status` field exists in `approval.request` model
#                 approvers_info.append({'name': name, 'status': status})
#             return approvers_info
#         return None

# class PurchaseOrderApproverDetail(models.Model):
#     _name = 'purchase.order.approver.detail'
#     _description = 'Purchase Order Approver Detail'

#     purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')
#     name = fields.Char(string='Approver Name')
#     status = fields.Char(string='Status')

# # In your view, you can display the approver_table field using the `widget="html"` option to render the HTML content.
# from odoo import models, fields, api

# class PurchaseOrder(models.Model):
#     _inherit = 'purchase.order'
    
#     approval_request_id = fields.Many2one('approval.request', string='Approval Request')
#     approvers_details = fields.One2many('purchase.order.approver.detail', 'purchase_order_id', string='Approvers Details')

#     @api.onchange('approval_request_id')
#     def _onchange_approval_request_id(self):
#         if self.approval_request_id:
#             self._update_approvers_details()

#     def _update_approvers_details(self):
#         self.ensure_one()
#         ApproverDetail = self.env['purchase.order.approver.detail']
        
#         # Clear existing approvers' details
#         self.approvers_details.unlink()
        
#         # Fetch new approvers' details
#         approvers_info = self._get_approvers_info(self)
        
#         # Add new approvers' details
#         if approvers_info:
#             for approver in approvers_info:
#                 ApproverDetail.create({
#                     'purchase_order_id': self.id,
#                     'name': approver['name'],
#                     'status': approver['status']
#                 })

#     def _get_approvers_info(self, record):
#         if record.approval_request_id and record.approval_request_id.approver_ids:
#             approvers_info = []
#             for approver in record.approval_request_id.approver_ids:
#                 name = approver.user_id.name
#                 status = approver.status  # Assuming `status` field exists in `approval.request` model
#                 approvers_info.append({'name': name, 'status': status})
#             return approvers_info
#         return None

# class PurchaseOrderApproverDetail(models.Model):
#     _name = 'purchase.order.approver.detail'
#     _description = 'Purchase Order Approver Detail'

#     purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', required=True, ondelete='cascade')
#     name = fields.Char(string='Approver Name', required=True)
#     status = fields.Char(string='Status', required=True)
from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    approval_request_id = fields.Many2one('approval.request', string='Approval Request')
    approvers_names = fields.Text(string='Approvers Names', compute='_compute_approvers_info')
    approvers_statuses = fields.Text(string='Approvers Statuses', compute='_compute_approvers_info')

    @api.depends('approval_request_id')
    def _compute_approvers_info(self):
        for order in self:
            if order.approval_request_id:
                approvers = order.approval_request_id.approver_ids
                names = ", ".join([approver.user_id.name for approver in approvers])
                statuses = ", ".join([approver.status for approver in approvers])
                order.approvers_names = names
                order.approvers_statuses = statuses
            else:
                order.approvers_names = ""
                order.approvers_statuses = ""

from odoo import models, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        purchase_order = super(PurchaseOrder, self).create(vals)
        if purchase_order.approval_request_id:
            purchase_order._compute_approvers_info()
        return purchase_order
'''
############################Grant APProve############################################
iif record.approval_request_id:
    approval_request = record.approval_request_id
    current_user = env.user

    # Check if the current user is in the list of approvers of the approval category
    approvers = approval_request.category_id.approver_ids
    if current_user in approval_request.approver_ids.mapped('user_id'):
    
        
            approval_request.action_approve()
        
    else:
        raise ValueError("The current user is not in the list of approvers.")
else:
    raise ValueError("The purchase order does not have an associated approval request.")




#######################Approval Request##################################


approval_request = env['approval.request'].create({
    'name': record.name,  # Use the name of the created purchase order
    'request_owner_id': env.user.id,
    'category_id': record.x_studio_approval_scenario.id,  # Replace with your approval category ID
    'reason': 'This is an automated approval request.',
})
approval_request.write({'request_status': 'pending'})
# Update the purchase order with the created approval request ID
record.write({'approval_request_id': approval_request.id})
#Define the code to create approval request and notify approvers


# Send activities to notify the approvers
users= record.approval_request_id.approver_ids
user_ids=[]
contract=record
for user in users:
    user_id=user.user_id.id
    record.notification(user_id,contract) 

######################################refuse##################################
if record.approval_request_id:
    approval_request = record.approval_request_id
    current_user = env.user

    # Check if the current user is in the list of approvers of the approval category
    approvers = approval_request.category_id.approver_ids
    if current_user in approval_request.approver_ids.mapped('user_id'):
    
        
            approval_request.action_refuse()
        
    else:
        raise ValueError("The current user is not in the list of approvers.")
else:
    raise ValueError("The purchase order does not have an associated approval request.")






'''