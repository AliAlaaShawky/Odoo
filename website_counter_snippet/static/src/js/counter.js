// odoo.define('website_counter_snippet.counter', ['require', 'web.public.widget'], function (require) {
//     'use strict';

//     var publicWidget = require('web.public.widget');

//     publicWidget.registry.counterSnippet = publicWidget.Widget.extend({
//         selector: '.o_website_counter_snippet',
//         start: function () {
//             this._super.apply(this, arguments);
//             this._animateCounter();
//         },
//         _animateCounter: function () {
//             var counters = document.querySelectorAll('.counter');
//             counters.forEach(counter => {
//                 counter.innerText = '0';

//                 const updateCounter = () => {
//                     const target = +counter.getAttribute('data-target');
//                     const c = +counter.innerText;

//                     const increment = target / 200;

//                     if (c < target) {
//                         counter.innerText = `${Math.ceil(c + increment)}`;
//                         setTimeout(updateCounter, 30);
//                     } else {
//                         counter.innerText = target;
//                     }
//                 };

//                 updateCounter();
//             });
//         }
//     });

//     return publicWidget.registry.counterSnippet;
// });
