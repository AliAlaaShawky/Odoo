from lxml import etree
from odoo import models, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)

        if view_type == 'form':
            is_group_user = self.env.user.has_group('base.group_user')
            is_group_system = self.env.user.has_group('base.group_system')
            if is_group_user:
                for node in arch.xpath("//field[@name='partner_id']"):
                    node.set('options', "{'no_create': True, 'no_edit': True}")
                for node in arch.xpath("//field[@name='product_template_id']"):
                    node.set('options', "{'no_create': True, 'no_edit': True}")

            #     print('user',is_group_user)
            # elif is_group_system:
            #     for node in arch.xpath("//field[@name='partner_id']"):
            #         node.set('options', "{'no_create': False, 'no_edit': False}")
            #     for node in arch.xpath("//field[@name='product_template_id']"):
            #         node.set('options', "{'no_create': False, 'no_edit': False}")
            #     print('admin',is_group_system)

        return arch, view
