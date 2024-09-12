from odoo import models, fields ,api
from odoo.exceptions import ValidationError 
from datetime import datetime
class MetaData(models.Model):
    _name='enduser'
    name=fields.Char(required=True ,size=30)
    company=fields.Char(required=True ,size=30)
    address=fields.Char(required=True ,size=60)
    work_email=fields.Char(required=True ,size=30)
    work_mobile=fields.Char(required=True ,size=11)
    
    

    ##SQL constrains
    _sql_constraints=[
        ('unique_name','unique("name")','This name is already exist!')
    ]
    








