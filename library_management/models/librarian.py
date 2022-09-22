from odoo import fields, models,api,_
from datetime import date


class Librarian(models.Model):
    _name = "librarian.librarian" #This will be the table name.
    _description = "This is master Table to store the Librarians"

    name=fields.Char(string="Name")
    gender=fields.Selection([('Male','Male'),('Female','Female')],string="Gender")
    dob=fields.Date(string="Birthdate")
    age=fields.Integer(string="Age",compute="_compute_age")
    date_of_joining=fields.Date(string="Date of Joining")
    experience=fields.Float(string="Current Experience(In Years)",compute="_compute_exp")


    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            rec.age =0
            if rec.dob:
                birthDate = rec.dob
                today = date.today()
                age = today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day))
                rec.age = age



    @api.depends('date_of_joining')
    def _compute_exp(self):
        for rec in self:
            rec.experience =0
            if rec.date_of_joining:
                doj= rec.date_of_joining
                today = date.today()
                exp = today.year - doj.year -((today.month, today.day) < (doj.month, doj.day))
                rec.experience = exp           
    

    
    