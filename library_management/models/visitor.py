from odoo import fields, models,api,_
from datetime import date


class Visitor(models.Model):
    _name = "visitor.visitor" #This will be the table name.
    _description = "This stores data of Visitor"

    name=fields.Char(string="Name",required="1")
   
