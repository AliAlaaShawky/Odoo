from odoo import http
from odoo.http import request
import json
import logging

_logger = logging.getLogger(__name__)

class YeastarController(http.Controller):

    @http.route('/jsonrpc/handle_incoming_call', type='json', auth='public', methods=['POST'], csrf=False)
    def handle_incoming_call(self):
        # Log the request to check if it's coming in
        _logger.info('Incoming call received from: %s', request.httprequest.remote_addr)

        # Check if the request is coming from Yeastar's IP address
        yeastar_ip = '192.168.10.150'
        incoming_ip = request.httprequest.remote_addr

        if incoming_ip != yeastar_ip:
            _logger.warning('Unauthorized request from IP: %s', incoming_ip)
            return {"error": "Unauthorized request source"}

        # Process Yeastar's incoming call
        data = json.loads(request.httprequest.data)
        phone_number = data.get('phone_number')

        if not phone_number:
            _logger.error('No phone number provided in the request.')
            return {"error": "No phone number provided"}

        # Log the phone number
        _logger.info('Processing incoming call for phone number: %s', phone_number)

        # Search for contact by phone number
        contact = request.env['res.partner'].sudo().search([('phone', '=', phone_number)], limit=1)

        if contact:
            _logger.info('Contact found: %s', contact.name)
            # If contact is found, return the URL to open the contact in Odoo
            contact_url = f"http://192.168.1.201:8069/web#id={contact.id}&model=res.partner&view_type=form&cids=1"
            return {"url": contact_url}
        else:
            _logger.info('No contact found for phone number %s, creating CRM lead.', phone_number)
            # If no contact is found, create a CRM lead
            lead_vals = {
                'name': f"Lead for {phone_number}",
                'phone': phone_number,
                'type': 'lead',
                'description': f"Incoming call from {phone_number}",
            }
            new_lead = request.env['crm.lead'].sudo().create(lead_vals)
            return {"message": "Lead created", "lead_id": new_lead.id}
