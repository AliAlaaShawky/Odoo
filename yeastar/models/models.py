# from odoo import models, fields, api

# import requests
# import logging
# import time
# import warnings
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# warnings.filterwarnings('ignore', category=InsecureRequestWarning)
# _logger = logging.getLogger(__name__)

# class IncomingCallLog(models.Model):
#     _name = 'incoming.call.log'
#     _description = 'Log of Incoming Calls'

#     user_id = fields.Many2one('res.partner', string="User")
#     caller_id = fields.Char(string="Caller ID")
#     extension_number = fields.Char(string="Extension Number")
#     call_time = fields.Datetime(string="Call Time", default=fields.Datetime.now)
#     yeastar_access_token = None
#     yeastar_token_expiry = 0
#     @classmethod
#     def get_yeastar_access_token(cls):
#         """Fetch or refresh the access token from Yeastar"""
#         current_time = time.time()
#         if not cls.yeastar_access_token or current_time > cls.yeastar_token_expiry:
#             yeastar_api_url = "https://192.168.10.150:8088/openapi/v1.0/get_token"
#             headers = {
#                 "Content-Type": "application/json",
#                 "User-Agent": "OpenAPI"
#             }
#             data = {
#                 "username": "XnV2ywkRYxwqmuVw72UqJEyrX7J1X2Qc",
#                 "password": "gmx33IUdt6N8HStoiLpJ1o3L21hIH3rX"
#             }
#             try:
#                 response = requests.post(yeastar_api_url, headers=headers, json=data, verify=False, timeout=30)
#                 if response.status_code == 200:
#                     token_data = response.json()
#                     cls.yeastar_access_token = token_data.get('access_token')
#                     cls.yeastar_token_expiry = current_time + 1200  # Token expires in 20 minutes
#                     _logger.info(f"New access token fetched: {cls.yeastar_access_token}")
#                 else:
#                     _logger.error(f"Failed to get token. Status code: {response.status_code}")
#             except requests.RequestException as e:
#                 _logger.error(f"Error while fetching token: {e}")
#         return cls.yeastar_access_token

#     @api.model
#     def poll_yeastar_for_calls(self):
#         """Poll Yeastar API for call logs and process incoming calls"""
#         token = self.get_yeastar_access_token()
#         if not token:
#             _logger.error("No access token available to poll Yeastar API.")
#             return

#         query_url = f"https://192.168.10.150:8088/openapi/v1.0/call/query?access_token={token}"
#         headers = {
#             "Content-Type": "application/json",
#             "User-Agent": "OpenAPI"
#         }
#         try:
#             response = requests.get(query_url, headers=headers, verify=False, timeout=30)
#             if response.status_code == 200:
#                 response_json = response.json()
#                 if response_json.get("errcode") == 0:
#                     self.process_incoming_calls(response_json.get("data", []))
#                 else:
#                     _logger.error(f"API error: {response_json.get('errmsg')}")
#             else:
#                 _logger.error(f"Failed to query Yeastar API. Status code: {response.status_code}")
#         except requests.RequestException as e:
#             _logger.error(f"Error while querying Yeastar API: {e}")

#     def process_incoming_calls(self, call_data):
#         """Process each incoming call and log it in Odoo"""
#         for call in call_data:
#             for member in call.get("members", []):
#                 extension_info = member.get("extension", {})
#                 extension_number = extension_info.get("number")
#                 channel_id = extension_info.get("channel_id")
#                 member_status = extension_info.get("member_status")

#                 user = self.env['res.partner'].sudo().search([('phone', '=', extension_number)], limit=1)
#                 if user and member_status in ["RING", "ALERT"]:
#                     self.create({
#                         'user_id': user.id,
#                         'caller_id': member.get("caller_id"),
#                         'extension_number': extension_number,
#                         'call_time': fields.Datetime.now(),
#                     })
#                     _logger.info(f"Inbound call for extension {extension_number}, user {user.name}")

#     @api.model
#     def schedule_polling(self):
#         """Scheduled job to poll Yeastar API at regular intervals"""
#         self.poll_yeastar_for_calls()
#     def action_confirm(self):
#         # Implement the logic for answering the call
#         print("Accepting")
#         return True

#     def action_refuse_call(self):
#         # Implement the logic for refusing the call
#         print("Reject")
#         return True
#     @api.model
#     def create(self, vals):
#         """Override the create method to trigger the notification when a new call log is created."""
#         record = super(IncomingCallLog, self).create(vals)
#         record.notify_incoming_call()
#         return record

#     @api.model
#     def notify_incoming_call(self):
#         """Trigger real-time notification using the Bus framework for a new incoming call."""
#         _logger.info("Running cron job to check for incoming calls")
#         try:
#             # Fetch the latest call logs
#             incoming_calls = self.search([], order="call_time desc", limit=1)

#             if incoming_calls:
#                 for call in incoming_calls:
#                     _logger.info(f"Processing incoming call for extension: {call.extension_number}, Caller: {call.caller_id}")

#                     # Notify the user in real time through Odoo's Bus framework
#                     self.env['bus.bus']._sendone(
#                         (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),  # User to notify
#                         'incoming_call_notification',  # Notification channel
#                         {
#                             'user_id': call.user_id.id,
#                             'caller_id': call.caller_id,
#                             'extension_number': call.extension_number,
#                             'call_time': call.call_time,
#                         }
#                     )
#                     _logger.info(f"Bus notification sent for user {call.user_id.id}")

#         except Exception as e:
#             _logger.error(f"Error processing incoming call: {e}")
#             raise
from odoo import api, models
from odoo.http import request

from odoo import api, models
from odoo.http import request

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        # Print options directly passed into the method
        print("Options passed:", options)

        # Get the action_id from the options
        action_id = options.get('action_id')

        print('Get action_id:', action_id)
        print('menu_id' not in request.params)
        print('request', request)
        print('request.params', request.params)
        contact_id = request.params.get('id')
        print(contact_id, 'contact_id')
        existing_lead = self.env['crm.lead'].search([('partner_id', '=', contact_id)], limit=1)
            
        if not existing_lead and not action_id and 'menu_id' not in request.params :  # Example condition for specific action_id
            # Logic to create a CRM Lead
            print("Here is the CRM Lead")
            partner = self.env['res.partner'].browse(contact_id)
            lead_values = {
                    'name': f'Lead from {partner.name}',  # Lead name based on the partner's name
                    'partner_id': partner.id,
                    'contact_name': partner.name,
                    'type': 'lead',
                }
            self.env['crm.lead'].create(lead_values)

        return arch, view
