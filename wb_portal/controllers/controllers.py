# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import  request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo import models, fields ,api
from odoo.exceptions import UserError
import werkzeug

class WebSupportPortal(CustomerPortal):
    

   from odoo import http
from odoo.http import request
import werkzeug.wrappers

class MyController(http.Controller):

    from odoo import http
from odoo.http import request
import werkzeug.wrappers

class WebSupportPortal(http.Controller):

    @http.route(['/my/ps'], type='http', auth='public', website=True)
    def WebSupportPortalView(self, **kw):
        user = request.env.user
        if user._is_public():
            return werkzeug.wrappers.Response('Access Denied: Please log in as a portal user.', status=403)

        employee = user.partner_id.employee_id or user.employee_id
        if not employee:
            return werkzeug.wrappers.Response('Access Denied: No employee linked to user.', status=403)

        is_department_manager = request.env['hr.employee'].search_count([('parent_id', '=', employee.id)]) > 0
        if is_department_manager:
            employees_in_department = request.env['hr.employee'].search([('department_id', '=', employee.department_id.id)])
            tickets = request.env['hr.leave'].search([('employee_id', 'in', employees_in_department.ids)])
            return request.render('wb_portal.manager_support_portal', {
                'ticket': tickets,
                'page_name_view': 'ticket_list_view',
            })

        tickets = request.env['hr.leave'].search([('employee_id', '=', employee.id)])
        return request.render('wb_portal.support_portal', {
            'ticket': tickets,
            'page_name_view': 'ticket_list_view',
        })

    @http.route('/my/approve/<int:ticket_id>', type='http', auth='user', website=True)
    def approve_ticket(self, ticket_id, **kwargs):
        ticket = request.env['hr.leave'].sudo().browse(ticket_id)
        if ticket:
            ticket.action_approve()
        return request.redirect('/my/ps')

    @http.route('/my/edit/<int:ticket_id>', type='http', auth='user', website=True)
    def edit_ticket(self, ticket_id, **kwargs):
        user = request.env.user
        tickets = request.env['hr.leave'].sudo().browse(ticket_id)
        # Get the name of the currently logged-in user
        user_name = user.name
        # Get the current user's employee record
        employee = user.partner_id.employee_id or user.employee_id
        leave_types = request.env['hr.leave.type'].sudo().search([])
        employee_id = employee.id if employee else False
        if tickets.state =='confirm':
            return request.render('wb_portal.api_data_display_form', {
            'ticket': tickets,
            'user_name': user_name,
            'employee_id': employee_id,
            'leave_types': leave_types,
            'ticket_id':ticket_id,
            'page_name_view': 'list_timeoff',
                })
        return request.redirect('/my/ps')

    @http.route('/my/approve/<int:ticket_id>', type='http', auth='user', website=True)
    def approve_ticket(self, ticket_id, **kwargs):
        ticket = request.env['hr.leave'].sudo().browse(ticket_id)
        if ticket:
            ticket.action_approve()
        return request.redirect('/my/ps')

    @http.route(['/my/timeoff'],type='http', auth='public', website=True)
    def WebTimePortalView(self, **kw):
        user = request.env.user
        if user._is_public():
            # If the user is not authenticated (public user), deny access
            return werkzeug.wrappers.Response('Access Denied: Please log in as a portal user.', status=403)
        employee = user.partner_id.employee_id or user.employee_id
        if not employee:
            return werkzeug.wrappers.Response('Access Denied: No employee linked to user.', status=403)
        
        # Get the name of the currently logged-in user
        user_name = user.name
        # Get the current user's employee record
        employee = user.partner_id.employee_id or user.employee_id
        employee_id = employee.id if employee else False

        # Get available leave types (you can add conditions to filter based on user)
        leave_types = request.env['hr.leave.type'].sudo().search([])

        return request.render('wb_portal.ticket_view_form', {
            'user_name': user_name,
            'employee_id': employee_id,
            'leave_types': leave_types,
            'page_name':'list_timeoff',
        })
    @http.route('/create/timeoff', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def update_timeoff(self, **kwargs):
        user = request.env.user
        if user._is_public():
            # If the user is not authenticated (public user), deny access
            return werkzeug.wrappers.Response('Access Denied: Please log in as a portal user.', status=403)
        
        
        user = request.env.user
        employee = user.partner_id.employee_id or user.employee_id
        employee_id = employee.id
        holiday_status_id = int(kwargs.get('holiday_status_id', 0))
        request_date_from = kwargs.get('request_date_from')
        request_date_to = kwargs.get('request_date_to')
        request_hour_from = kwargs.get('request_hour_from')
        request_hour_to = kwargs.get('request_hour_to')
        half_day = kwargs.get('half_day')
        name = kwargs.get('name')

        if not request_date_from or not request_date_to:
            raise UserError("Please provide both 'Request Date From' and 'Request Date To'.")

        if half_day:
            request_hour_from = '0'
            request_hour_to = '4' if half_day == 'morning' else '8'

        leave_record = request.env['hr.leave'].create({
            'employee_id': employee_id,
            'holiday_status_id': holiday_status_id,
            'request_date_from': request_date_from,
            'request_date_to': request_date_to,
            'request_hour_from': request_hour_from,
            'request_hour_to': request_hour_to,
            'name': name,
        })

        return request.render('wb_portal.success_page', {'page_name':'list_timeoff',})
   

    @http.route('/edit/timeoff', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def edit_timeoff(self, **kwargs):
        user = request.env.user
        if user._is_public():
            # If the user is not authenticated (public user), deny access
            return werkzeug.wrappers.Response('Access Denied: Please log in as a portal user.', status=403)

        employee = user.partner_id.employee_id or user.employee_id
        holiday_status_id = int(kwargs.get('holiday_status_id', 0))
        request_date_from = kwargs.get('request_date_from')
        request_date_to = kwargs.get('request_date_to')
        request_hour_from = kwargs.get('request_hour_from')
        request_hour_to = kwargs.get('request_hour_to')
        half_day = kwargs.get('half_day')
        name = kwargs.get('name')

        if not request_date_from or not request_date_to:
            raise UserError("Please provide both 'Request Date From' and 'Request Date To'.")

        if half_day:
            request_hour_from = '0'
            request_hour_to = '4' if half_day == 'morning' else '8'

        leave_id = int(kwargs.get('ticket_id'))
        leave_record = request.env['hr.leave'].browse(leave_id)
        leave_record.write({
            'holiday_status_id': holiday_status_id,
            'request_date_from': request_date_from,
            'request_date_to': request_date_to,
            'request_hour_from': request_hour_from,
            'request_hour_to': request_hour_to,
            'name': name,
        })

        return request.render('wb_portal.success_page', {'page_name': 'list_timeoff'})

    
      
class TimeOff(models.Model):
    _name='timeoff'
    _description='Your request is received'
    _inherit=['hr.leave']
    name = fields.Char('Description', compute='_compute_description', inverse='_inverse_description', search='_search_description', compute_sudo=False, copy=False)
    private_name = fields.Char('Time Off Description', groups='hr_holidays.group_hr_holidays_user')
    
    employee_id = fields.Many2one(
        'hr.employee', compute='_compute_from_employee_ids', store=True, string='Employee', index=True, readonly=False, ondelete="restrict",
        tracking=True, compute_sudo=False,
        domain=lambda self: self._get_employee_domain())
    request_date_from = fields.Date('Request Start Date')
    request_date_to = fields.Date('Request End Date')
    


# class WbPortal(http.Controller):
#     @http.route('/wb_portal/wb_portal', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wb_portal/wb_portal/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wb_portal.listing', {
#             'root': '/wb_portal/wb_portal',
#             'objects': http.request.env['wb_portal.wb_portal'].search([]),
#         })

#     @http.route('/wb_portal/wb_portal/objects/<model("wb_portal.wb_portal"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wb_portal.object', {
#             'object': obj
#         })

