from odoo import models, fields, api


class PurchaseOrderWizard(models.TransientModel):
    _name = 'purchase.order.wizard'
    _description = 'Purchase Order Wizard'

    option = fields.Selection([
        ('new', 'Create New Purchase Order'),
        ('existing', 'Choose Existing Purchase Order')
    ], string='Option', required=True, default='new')
    
    order_id = fields.Many2one('purchase.order', 'Order')
    order_line_ids = fields.One2many(
        'purchase.order.line', related='order_id.order_line', string='Products', readonly=True)
    customer_id = fields.Many2one('res.partner', 'Customer', required=True, default=lambda self: self._default_customer_id(), readonly=True)
    total_price=fields.Float('TotalPrice', required=True, compute='_default_total_price')
    @api.model
    def _default_customer_id(self):
        return self.env.context.get('default_customer_id')
    @api.onchange('order_id')
    def _default_total_price(self):
       for wizard in self:
            if wizard.order_id:
                total_price = sum(line.price_total for line in wizard.order_id.order_line)
            else:
                total_price = 0.0
            
            # Update the 'total_price' field on the wizard
            wizard.update({
                'total_price': total_price,
            })

    def action_confirm(self):
        if self.option == 'new':
            # Assuming you have a variable `partner_id` and `sales_order_id` available
            # Replace `partner_id` and `sales_order_id` with actual values or variables
            partner_id = self.customer_id.id  # Assuming self.partner_id is the vendor/partner record
            sales_order_id = self.env.context.get('active_id')
            sales_order = self.env['sale.order'].browse(sales_order_id)
            sales_order_id = sales_order.id  # Assuming self.id is the current sales order ID
            print(sales_order_id)
            return {
                'type': 'ir.actions.act_window',
                
                'name': 'Create Purchase Order',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_partner_id': partner_id,  # Set default_partner_id to fill vendor name
                    'default_sales_order_id': sales_order_id,  # Set default_sales_order_id for sales order link
                },
            }
        else:
            sales_order_id = self.env.context.get('active_id')
            if sales_order_id:
                sales_order = self.env['sale.order'].browse(sales_order_id)
                print('sales_order',sales_order)
                set_sales_id=self.env['purchase.order'].browse(self.order_id.id)
                print('set_sales_id',set_sales_id)
                set_sales_id.write({'sales_order_id': sales_order.id,})

                # Find or create the "Offer" product
                offer_product = self.env['product.product'].search([('name', '=', 'Offer')], limit=1)
                if not offer_product:
                    # Create "Offer" product if it doesn't exist
                    offer_product = self.env['product.product'].create({
                        'name': 'Offer',
                        'detailed_type': 'service',  # Adjust as per your product type
                        'sale_ok': True,
                        'taxes_id':None,
                        'list_price': None,

                    })
                # Create a new order line for the "Offer" product
                line_data = {
                    'order_id': sales_order_id,
                    'product_id': offer_product.id,
                    'name': f'Offer from {self.order_id.name}',
                    'product_uom_qty': 1,
                    'tax_id':None,
                    'price_unit': -self.total_price,  # Negative price
                    
                }
                self.env['sale.order.line'].create(line_data)
                return True
            else:
                print(f'No active sales order found')
                return False