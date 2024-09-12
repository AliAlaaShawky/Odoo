from odoo import models, fields, api,_
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    

    def action_get_offer_button(self):
            _logger.info("action_get_offer_button called")
            try:
                _logger.info(f"Current context: {self.env.context}")
                customer_id = self.partner_id.id
                _logger.info(f"Customer ID: {customer_id}")
                return {
                    'type': 'ir.actions.act_window',
                    'tag': 'reload',
                    'name': 'Purchase Order Options',
                    'res_model': 'incoming.call.log',
                    'view_mode': 'form',
                    'target': 'new',
                    'context': {
                        'default_customer_id': customer_id,
                        **self.env.context
                    },
                }
            except Exception as e:
                _logger.error(f"Error in action_get_offer_button: {e}")
                raise

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    sales_order_id = fields.Many2one('sale.order', string="Sales Order",readonly=True)
    is_purchase_admin = fields.Boolean(string="Is Purchase User", compute='_compute_is_purchase_user')
    offer_added = fields.Boolean("Offer Added", default=False)

    #check the user permision to allow edit for admins only
    @api.model
    def _compute_is_purchase_user(self):
        for record in self:
            if self.env.user.has_group('purchase.group_purchase_manager'):  # Replace with your actual group name
                record.is_purchase_admin = True
            else:
                record.is_purchase_admin = False

    def create_sales_order(self):
        # Search for an existing "Offer" product
        offer_product = self.env['product.product'].search([('name', '=', 'Offer')], limit=1)
        
        if not offer_product:
            # Create "Offer" product if it doesn't exist
            offer_product = self.env['product.product'].create({
                'name': 'Offer',
                'detailed_type': 'service',  # Adjust as per your product type
                'sale_ok': True,
                'taxes_id': None,
                'list_price': None,
            })

        # Create a new Sales Order
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'order_line': [(0, 0, {
                'product_id': offer_product.id,
                'name': f'Offer from {self.name}',
                'product_uom_qty': 1,
                'price_unit': -self.amount_total,  # Negative price
                'tax_id': None,
                
            })],
        })

        # Update the Purchase Order with the Sales Order ID
        self.sales_order_id = sale_order.id

        return {
            'type': 'ir.actions.act_window',
            'tag': 'reload',
            'name': 'Create Sales Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'new',
            'res_id': sale_order.id,  # Open the newly created Sales Order form view
        }
        
    def button_confirm(self):
        res = super(PurchaseOrder, self).button_confirm()
        
        # Call the add_as_offer method for each purchase order in the recordset
        for order in self:
            if  order.offer_added==False:
                order.add_as_offer()
                     
        return res

    def add_as_offer(self):
        # Check if the offer has already been added
        if self.offer_added:
            raise UserError(_("The offer has already been added to this order."))

        # Search for the associated sale order using the sales_order_id
        sale_order = self.env['sale.order'].browse(self.sales_order_id.id)
        
        

        # Search for the "Offer" product, create it if it doesn't exist
        offer_product = self.env['product.product'].search([('name', '=', 'Offer')], limit=1)
        
        if not offer_product:
            offer_product = self.env['product.product'].create({
                'name': 'Offer',
                'detailed_type': 'service',  # Adjust as per your product type
                'sale_ok': True,
                'taxes_id': None,
                'list_price': 0.0,
                
            })

        # Create a new offer product line for the "Offer" product
        line_data = {
            'product_id': offer_product.id,
            'name': f'Offer from {self.name}',
            'product_uom_qty': 1,
            'price_unit': -self.amount_total,  # Negative price
            'tax_id': [(6, 0, [])],  # Ensure taxes_id is properly set
            
        }

        # Add the offer line to the existing sale order
        sale_order.write({'order_line': [(0, 0, line_data)]})

        # Mark the offer as added
        self.offer_added = True

        # Log the addition of the offer for tracking
        _logger.info("Offer added to Sales Order ID: %s", sale_order.id)
        

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'target': 'new',
            'res_id': sale_order.id,
        }
    def remove_the_offer(self):
        sale_order = self.env['sale.order'].browse(self.sales_order_id.id)
        
        if not sale_order:
            raise UserError(_("Associated Sales Order not found"))
        if  sale_order.state=="sale":
            raise UserError(_("Associated Sales Order should be a not confirmed order"))

        offer_product = self.env['product.product'].search([('name', '=', 'Offer')], limit=1)
        
        if offer_product:
            # Find the offer line in the sale order that matches both product_id and price_unit
            offer_lines = sale_order.order_line.filtered(
                lambda l: l.product_id == offer_product and l.price_unit == -self.amount_total and l.name ==f'Offer from {self.name}'
            )
            
            if offer_lines:
                # Unlink (delete) the offer line(s)
                offer_lines.unlink()

        # Update the fields after removing the offer line
        self.sales_order_id = None
        self.offer_added = False
    @api.model
    def create(self, vals):
        # Call super to create the purchase order
        po = super(PurchaseOrder, self).create(vals)
        
        # Check if sales_order_id is set
        if po.sales_order_id:
            

            # Trigger confirm order method
            po.button_confirm()
            self.notify_message(title="Added as Offer", type_notify='success', message="The order is added successfully")
            # Lock the order by setting it to 'purchase' state
            po.write({'state': 'done'})


        return po



    def notify_message(self, title, type_notify, message):
        print("notify message")
        notification = {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _(title),
                'type': type_notify,
                'message': _(message),
                'sticky': True,
            }
        }
        return notification


        