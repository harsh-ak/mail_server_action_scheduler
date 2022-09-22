from odoo import fields, models,api,_
from datetime import date
from random import randint
from odoo.exceptions import ValidationError
import base64,sys


class SaleOrder(models.Model):
	_inherit='sale.order'


	def action_confirm(self):
		template_id = self.env.ref('library_management.send_mail_template').id
		print("___________________________",template_id)
		self.env['mail.template'].browse(template_id).send_mail(self.id,force_send=True)
		return super(SaleOrder,self).action_confirm() 