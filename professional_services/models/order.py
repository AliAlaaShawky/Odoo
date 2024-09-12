from odoo import models, fields ,api
from odoo.exceptions import ValidationError 
from datetime import datetime
class MetaData(models.Model):
    _name='order'
    name=fields.Char(required=True ,size=30)
    company=fields.Char(required=True ,size=30)
    address=fields.Char(required=True ,size=60)
    
    
    

    








