from odoo import models, fields ,api
from odoo.exceptions import ValidationError 
from datetime import datetime
class MetaData(models.Model):
    _name='tags'
    name=fields.Char(required=True ,size=30)
    ##SQL constrains
    _sql_constraints=[
        ('unique_name','unique("name")','This name is already exist!')
    ]
    








