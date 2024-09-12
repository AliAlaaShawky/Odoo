from odoo import http
from odoo.http import request

class PricelistController(http.Controller):

    @http.route('/calculate_prices/<int:pricelist_id>', type='json', auth="user", website=True)
    def calculate_prices(self, pricelist_id, **kwargs):
        pricelist = request.env['product.pricelist'].browse(pricelist_id)
        if not pricelist:
            return {'error': 'Invalid pricelist ID'}

        price_list = pricelist.calculate_product_prices(pricelist_id)
        return {'prices': price_list}
