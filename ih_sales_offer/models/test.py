
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    sale_order_date = fields.Datetime(string='Sale Order Date', readonly=True)

    location_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Source Warehouse',
	required=True,
       
    )
    available_quantity = fields.Float(
        string='Available Quantity',
        compute='_compute_available_quantity',
        store=True
    )
    @api.depends('order_line.product_id', 'order_line.product_uom_qty', 'location_id')
    def _compute_available_quantity(self):
        for order in self:
            available_qty = 0.0
            if order.location_id:
                warehouse_main_location = order.location_id.view_location_id
                warehouse_locations = self.env['stock.location'].search([
                    ('id', 'child_of', warehouse_main_location.id)
                ])
                
                for line in order.order_line:
                    if line.product_id:
                        quants = self.env['stock.quant'].read_group(
                            [('product_id', '=', line.product_id.id),
                             ('location_id', 'in', warehouse_locations.ids)],
                            ['quantity', 'reserved_quantity'],
                            ['product_id']
                        )
                        
                        total_available_qty = sum(quant['quantity'] - quant['reserved_quantity'] for quant in quants)
                        available_qty += total_available_qty
            
            order.available_quantity = available_qty

   #set soucre warehouse
    @api.onchange('location_id')
    def _set_delivery_location(self):
        for record in self:
            if record.location_id:
                record.warehouse_id = record.location_id
 
    def _cron_update_sale_order_status(self):
        # Calculate the date one week ago from now
        week_ago = datetime.now() - timedelta(days=7)
        
        # Search for sales orders with sale_order_date older than a week and state 'sale'
        orders_to_cancel = self.search([
            ('state', '=', 'sale'),
            ('sale_order_date', '<', week_ago)
        ])
        
        _logger.info('Orders to cancel: %s', orders_to_cancel)

        # Cancel each order
        for order in orders_to_cancel:
            _logger.info('Cancelling order: %s', order.id)
            if order.state == 'sale':
                try:
                    order.write({'state': 'cancel'})
                    _logger.info('Order %s cancelled successfully', order.id)
                except Exception as e:
                    _logger.error('Failed to cancel order %s: %s', order.id, str(e))      
    #check the products available in the selected location
  
    def _check_stock_availability(self):
        for order in self:
            for line in order.order_line:
                if line.product_id and line.product_uom_qty > 0 and order.warehouse_id:
                    # Get the root location for the warehouse
                    warehouse_main_location = order.warehouse_id.view_location_id
                    
                    # Get all child locations of the main stock location
                    warehouse_locations = self.env['stock.location'].search([
                        ('id', 'child_of', warehouse_main_location.id)
                    ])
                    
                    # Debugging: Print location IDs and domain
                    print("Warehouse Location IDs:", warehouse_locations.ids)
                    print("Domain for read_group:", [('product_id', '=', line.product_id.id),
                                                    ('location_id', 'in', warehouse_locations.ids)])
                    
                    # Debug: Check if quants exist
                    quants_debug = self.env['stock.quant'].search([
                        ('product_id', '=', line.product_id.id),
                        ('location_id', 'in', warehouse_locations.ids)
                    ])
                    print("Quants Debug Result:", quants_debug)
                    
                    # Search for quants in all child locations of the warehouse
                    quants = self.env['stock.quant'].read_group(
                        [('product_id', '=', line.product_id.id),
                        ('location_id', 'in', warehouse_locations.ids)],
                        ['quantity', 'reserved_quantity'],
                        ['product_id']
                    )
                    
                    # Debugging: Print quants to check the results
                    print("Quants result:", quants)

                    # Calculate available quantity after considering reserved stock
                    total_available_qty = sum(quant['quantity'] - quant['reserved_quantity'] for quant in quants)
                    
                    # Prepare the total quantity and reserved quantity for the error message
                    total_quantity = sum(quant['quantity'] for quant in quants)
                    total_reserved_quantity = sum(quant['reserved_quantity'] for quant in quants)
                    
                    if total_available_qty < line.product_uom_qty and line.product_id.detailed_type =="product":
                        raise UserError(_('Insufficient stock for product %s in warehouse %s.\n'
                                        'Available quantity: %s\nReserved quantity: %s\n'
                                        'Total quantity: %s') % 
                                        (line.product_id.display_name, 
                                        order.warehouse_id.name, 
                                        total_available_qty, 
                                        total_reserved_quantity, 
                                        total_quantity))
    #check the products available in the selected location when confirm the order
    def action_confirm(self):
        self._check_stock_availability()
        return super(SaleOrder, self).action_confirm()
    #set value of sale_order_date
    def write(self, vals):
        if 'state' in vals and vals['state'] == 'sale':
            vals['sale_order_date'] = fields.Datetime.now()
        return super(SaleOrder, self).write(vals)
    #Extend expiration date
    def action_extend_sale_order_date(self):
        for order in self:
            if order.sale_order_date:
                new_date = order.sale_order_date + timedelta(weeks=1)
                order.sale_order_date = new_date
