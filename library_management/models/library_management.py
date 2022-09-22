from odoo import fields, models,api,_
from datetime import date


class LibraryManagement(models.Model):
    _name = "library.management" #This will be the table name.
    _description = "This is master table to store the Libraries"


    name=fields.Char(string="Library Name")
    property_type=fields.Selection([('Public','Public'),('Private','Private')])
    librarian_ids=fields.Many2many(comodel_name="librarian.librarian",string="Librarians")