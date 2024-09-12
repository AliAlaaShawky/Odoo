from odoo import models, fields ,api
from odoo.exceptions import ValidationError 
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)
class MetaData(models.Model):
    _name='ticket'
    _description='Your request is received'
    _inherit=['mail.thread','mail.activity.mixin']
    Ref=fields.Char(default='PS ticket',readonly=True)
    name=fields.Char(required=True , default='New Ticket',size=30,tracking=True)
    description=fields.Text()
    Assigned_to=fields.Many2one('hr.employee', string='Assigned Employee',required=True)
    urgent=fields.Boolean()
    priority = fields.Selection([("0", "low"), ("1", "middle"), ("2", "high"),("3", "very high")], default='0')
    customer=fields.Many2one('res.partner',string='Customer Name',required=True)
    customer_email=fields.Char(related='customer.email')
    
    end_user=fields.Many2one('enduser',required=True)
    end_user_email=fields.Char(related='end_user.work_email')
    datetime_created = fields.Datetime(default=fields.Datetime.now)   
    time_sheets=fields.Integer() 
    sales_order=fields.Many2one('sale.order',required=True)
    tags=fields.Many2many('tags',required=True)
    line_ids=fields.One2many('ticket.line','lineticket_id')
    time_ids=fields.One2many('ticket.time','time_ticket_id')
    Helpdesk_Team= fields.Selection(
        [
            ('operations','Operations'),
            ('support','Support'),
            ('pre sales','Pre sales'),
            
        ] ,  default='operations'
    )
    Type= fields.Selection(
        [
            ('incident_management','Incident Management'),
            ('change_management','Change Management'),
            ('request_for_information','Request for Information'),
            
        ] ,  default='incident_management'
    )
    stage= fields.Selection(
        [
            ('start','Start'),
            ('in_progress','In Progress'),
            ('pending','pending'),
            ('solved','Solved'),
            
        ] ,  default='start',tracking=True
    )
    ##SQL constrains
    _sql_constraints=[
        ('unique_name','unique("name")','This name is already exist!')
    ]
    

    @api.model
    def create(self, vals):
       res= super(MetaData, self).create(vals)
       if res.Ref =='PS ticket':
            res.Ref=self.env['ir.sequence'].next_by_code('Ticket_Sequence')
       return res 

    def action_start(self):
        for rec in self:
            rec.stage='start'
    def action_in_progress(self):
        for rec in self:
            rec.stage='in_progress'
    def action_pending(self):
        for rec in self:
            rec.stage='pending'
    def action_solved(self):
        for rec in self:
            rec.stage='solved'

class TicketLine(models.Model):
    _name='ticket.line'
    lineticket_id=fields.Many2one('ticket')
    description=fields.Text()
   


class TimeSheet(models.Model):
    _name='ticket.time'
    time_ticket_id=fields.Many2one('ticket')
    datetime_created = fields.Datetime(default=fields.Datetime.now)
    Assigned_to=fields.Many2one(related='time_ticket_id.Assigned_to')
    time_sheets=fields.Float()
    description=fields.Char()



