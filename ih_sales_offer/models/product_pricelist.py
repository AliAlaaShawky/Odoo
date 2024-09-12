

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    pricelist_info = fields.Text(string='Pricelist Info', compute='_compute_pricelist_info', store=True)
    pricelist_price_1 = fields.Float(compute='_compute_pricelist_prices', string='الجملة')
    pricelist_price_2 = fields.Float(compute='_compute_pricelist_prices', string='التجزئة')
    @api.depends('list_price','pricelist_info')
    def _compute_pricelist_prices(self):
        for product in self:
            pricelists = self.env['product.pricelist'].search([])
            if len(pricelists) >= 2:
                product.pricelist_price_1 = pricelists[0]._get_product_price(product, 1, False)
                product.pricelist_price_2 = pricelists[1]._get_product_price(product, 1, False)

    @api.depends('list_price')  # Triggers on the product's price change
    def _compute_pricelist_info(self):
        for product in self:
            pricelists = self.env['product.pricelist'].search([])
            price_info_str = []
            for pricelist in pricelists:
                # Calculate the price for the product in the context of this pricelist
                price = pricelist._get_product_price(product, 1.0, False)
                price_info_str.append(f"{pricelist.name}: {price:.2f}")
            # Join the lines with newline characters to create a multi-line string
            product.pricelist_info = "\n".join(price_info_str)

    @api.model
    def create(self, vals):
        product = super(ProductTemplate, self).create(vals)
        # Ensure that pricelist_info is computed for the newly created product
        product._compute_pricelist_info()
        return product

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        # Compute pricelist_info if the list_price field was updated
        if 'list_price' in vals:
            self._compute_pricelist_info()
        return result

    @api.model
    def update_all_products_pricelist_info(self):
        # This method will be used to update pricelist_info for all products
        all_products = self.search([])
        all_products._compute_pricelist_info()


class ProductPricelist(models.Model):
    _inherit = 'product.pricelist'

    @api.model
    def create(self, vals):
        pricelist = super(ProductPricelist, self).create(vals)
        # Trigger update for all products when a new pricelist is created
        self.env['product.template'].update_all_products_pricelist_info()
        return pricelist

    def write(self, vals):
        result = super(ProductPricelist, self).write(vals)
        # Trigger update for all products when a pricelist is updated
        self.env['product.template'].update_all_products_pricelist_info()
        return result
        
    def unlink(self):
        result = super(ProductPricelist, self).unlink()
        # Trigger update for all products when a pricelist is updated
        self.env['product.template'].update_all_products_pricelist_info()
        return result
