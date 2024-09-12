from odoo import models, fields ,api
from odoo.exceptions import ValidationError 
from datetime import datetime
class MetaData(models.Model):
    _name='team'
    name=fields.Char(required=True ,size=30)
    jop_title=fields.Char(required=True ,size=30)
    work_email=fields.Char(required=True ,size=30)
    work_mobile=fields.Char(required=True ,size=11)    
    Department= fields.Selection(
        [
            ('professional_services','Professional Services'),
            ('sales','Sales'),
            ('managment','Managment'),
            
        ] ,  default='professional_services'
    )
    

    ##SQL constrains
    _sql_constraints=[
        ('unique_name','unique("name")','This name is already exist!')
    ]
    








