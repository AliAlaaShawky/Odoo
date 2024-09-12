
from odoo import http
from odoo.http import request
from odoo.addons.project.controllers.portal import ProjectCustomerPortal as PortalCustomerView

class TaskPortal(PortalCustomerView):

    @http.route('/create/task', type='http', auth='user', website=True)
    def create_task_form(self, project_id=None,  search='',limit=10,**kw):
        user = request.env.user
        allowed_projects = self._get_allowed_projects(user)
        users = request.env['res.users'].sudo().search([])
        ticket_types = request.env['x_tickets_type'].sudo().search([])
        tag_types = request.env['project.tags'].sudo().search([])
        end_users = request.env['res.partner'].sudo().search([])
        priority=0
        users = request.env['res.partner'].sudo().search([], limit=limit)
        user_list = [{'id': user.id, 'text': user.name} for user in users]
        # Get the company name of the user's partner
        company_name = user.partner_id.parent_id.name
        
        # If the partner does not have a parent (company), return an empty recordset
        if not company_name:
            users_in_same_company=  user.partner_id
        else:
        # Search for all partners within the same company
             users_in_same_company = request.env['res.partner'].search([('parent_id.name', '=', company_name)])

        return request.render('IH_Project_Request.create_task_form', {
            'users': users,
            'project_id': int(project_id) if project_id else None,
            'allowed_projects': allowed_projects,
            'ticket_types':ticket_types,
            'tag_types':tag_types,
            'end_users':end_users,
            'priority':priority,
            'results': user_list,
            'users_in_same_company':users_in_same_company,
        })



    @http.route('/create/task/submit', type='http', auth='user', methods=['POST'], website=True, csrf=False)
    def submit_task(self, **post):
        user = request.env.user
        project_id = post.get('project_id')
        task_name = post.get('task_name')
        ticket_type_id = int(post.get('ticket_type_id', 0))
        tag_type_ids = post.get('tag_type_id')  # Get list of selected tag IDs
        end_user_id = post.get('end_user_id')  # Get list of selected tag IDs
        description = post.get('description')
        priority = post.get('priority')
        user_name_company_id =int(post.get('user_name_company_id', 0))  # Get list of selected tag IDs

        if priority:
            priority = str(priority)  # Convert priority to string
        else:
            priority = '0'  # Set default priority as string

        if isinstance(tag_type_ids, str):
            tag_type_ids = [int(tag_id) for tag_id in tag_type_ids.split(',')]
        else:
            tag_type_ids = [int(tag_id) for tag_id in tag_type_ids]

        valid_tag_type_ids = request.env['project.tags'].sudo().search([('id', 'in', tag_type_ids)]).ids
        if len(valid_tag_type_ids) != len(tag_type_ids):
            return request.redirect('/create/task?error=invalid_tag_ids')

        project = request.env['project.project'].sudo().search(
            [('id', '=', int(project_id))] if project_id.isdigit() else [('name', '=', project_id)], limit=1
        )

        if not project:
            return request.redirect('/create/task?error=project_not_found')
        partner_id = user.partner_id.id
        task_values = {
            'name': task_name,
            'user_ids': None,
            'partner_id': user_name_company_id,
            'description': description,
            'project_id': project.id,
            'x_studio_end_user_1': end_user_id,
            'tag_ids': [(6, 0, tag_type_ids)],
            'priority': priority,  # Ensure priority is a string
            'x_studio_ticket_type': ticket_type_id,
        }

        # Create the task and capture the task ID
        created_task = request.env['project.task'].sudo().create(task_values)

        # Redirect to the created task's page
        return request.redirect(f'/my/tasks/{created_task.id}')
    
    @http.route('/get_end_users', type='json', auth='user', website=True, method=['GET'])
    def get_end_users(self, search='', **kw):
        limit = request.params.get('limit') # Ensure 'limit' is an integer
        users = request.env['res.users'].sudo().search([('name', 'ilike', search)], limit=limit)
        user_list = [{'id': user.id, 'text': user.name} for user in users]
        return {'results': user_list}
    def _get_allowed_projects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Project = request.env['project.project']
        domain = self._prepare_project_domain()

        searchbar_sortings = self._prepare_searchbar_sortings()
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        project_ids = Project.search(domain).mapped('id')

        allowed_projects = Project.sudo().search([
            ('id', 'in', project_ids),
            #('sale_order_id.order_line.product_id.x_studio_support_services', '=', True),
            #('x_studio_contract.x_studio_selection_field_3e6_1hp8mrfn9', '=', "activate"),
        ], order=order)

        return allowed_projects
