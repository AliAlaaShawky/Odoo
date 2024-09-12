odoo.define('ih_sales_offer.calculate_prices', function (require) {
    "use strict";

    var ajax = require('web.ajax');

    function calculatePrices(pricelist_id) {
        ajax.jsonRpc('/calculate_prices/' + pricelist_id, 'call', {})
            .then(function (data) {
                if (data.error) {
                    alert(data.error);
                } else {
                    console.log('Calculated prices:', data.prices);
                    // Handle the prices as needed
                }
            });
    }

    return {
        calculatePrices: calculatePrices
    };
});
