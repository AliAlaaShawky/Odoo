from odoo import models, fields ,api
from odoo.exceptions import ValidationError 
from datetime import datetime
class MetaData(models.Model):
    _name='meta.data'
    name=fields.Char(required=True , default='New Name',size=20)
    description=fields.Text()
    postcode=fields.Text(required=True)
    date_availabilty=fields.Date(default=datetime.now().date())
    expected_price=fields.Float()
    selling_price=fields.Float()
    bedrooms=fields.Integer(required=True)
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean()
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orientatiion= fields.Selection(
        [
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West'),
        ] ,  default='north'
    )

    ##SQL constrains
    _sql_constraints=[
        ('unique_name','unique("name")','This name is already exist!')
    ]
    ## Valdiate the room numbers
    @api.constrains('bedrooms')
    def _check_bedrooms_value(self):
        for values in self:
            if values.bedrooms==0:
                raise ValidationError('Enter a valid number of bedrooms.')
    ##create record overwrite
    @api.model_create_multi
    def create(self,vals):
        res=super(MetaData,self).create(vals)
        print("Create method")
        return res
    @api.model
    def _search(self,domain,offset=0,limit=None,order=None,access_rights_uid=None):
        res=super(MetaData,self)._search(domain,offset=0,limit=None,order=None,access_rights_uid=None)
        print("search method")
        return res
    def write(self,vals):
        res=super(MetaData,self).write(vals)
        print("write method")
        return res
    def unlink(self):
        res=super(MetaData,self).unlink()
        print("delete method")
        return res








