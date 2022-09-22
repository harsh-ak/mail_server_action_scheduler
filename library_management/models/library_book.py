from odoo import fields, models,api,_
from datetime import date
from random import randint
from odoo.exceptions import ValidationError
import base64,sys


class LibraryBook(models.Model):
    _name = "library.book" #This will be the table name.
    _inherit=['mail.thread']
    _description = "This model stores the data about the Book information"

    name=fields.Char(string="Book Name")
    author=fields.Char(string="Author Name")
    isbn_no=fields.Char(string="ISBN No",readonly=True)
    image=fields.Image(string='Image',required=True)
    state=fields.Selection([('Good Condition','Good Condition'),('Scrapped','Scrapped')],default="Good Condition")
    sale_history_ids=fields.One2many(string="Sales History",comodel_name="sale.history.book",inverse_name="book_id")
    total=fields.Integer(string="Total Sales",compute='cal_sales')
    total_stock=fields.Integer(string="Total Stock")
    avail_stock=fields.Integer(string="Available Stock",compute="cal_stocks")
    partner_ids=fields.Many2many(string="Partner Name",comodel_name="res.partner")
    user_id=fields.Many2one(comodel_name="res.users",string="User Name")

    @api.model
    def create(self,vals):
        vals['isbn_no']=randint(10**(8-1),(10**8)-1)
        print("________________________",vals['isbn_no'])
        a=str(vals['isbn_no'])
        print("________________________",a)
        a=a.replace(","," ")
        print("________________________",a)
        vals['isbn_no']=int(a)
        print("________________________",vals['isbn_no'])
        res = super(LibraryBook, self).create(vals)
        return res


    def change_state(self):
        for rec in self:
            if rec.state=="Good Condition":
                rec.state="Scrapped"

    def cal_sales(self):
        for rec in self:
            sum=0
          #  sum1=0
            #res= self.env['sale.history.book'].search([('book_id', '=', self.id)])
            res=rec.sale_history_ids
            for record in res:
                sum+=record.Subtotal
         #       sum1+=record.quantity
        rec.total=sum
        #rec.stock-=sum1

    def demo(self):
        print("Clicked") 

    
    def cal_stocks(self):
        for rec in self:
            #rec.stock=0
            sum1=0
            rec.avail_stock=0
            res=rec.sale_history_ids
            for record in res:
                sum1+=record.quantity
       
            rec.avail_stock=rec.total_stock-sum1
            
       
  
    
    # @api.depends('avail_stock')
    # def cal_rem_stock(self):
    #     if self.avail_stock==0:
    #         self.total_stock=0
    #         print("_________________0 che")

    @api.constrains('image')
    def check_size(self):
        file_image = base64.b64decode(self.image)
        image_size = sys.getsizeof(file_image) * 0.0009765625
        if image_size > 50:
            raise ValidationError(_("You can't insert image with size more than 50 KB.\nYour Image Size: %s" % (image_size)))


    def send_mail(self):
        self.ensure_one()
        template_id = self.env.ref('library_management.library_book_email_template')
        print("_____________template_id",template_id.id)
        ctx = {
            'default_model': 'library.book',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            #'author':self.author,
            #'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            #'model_description': self.with_context(lang=lang).type_name,
        }
        print("\n\n\n\n111111111111111111111",ctx)
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }  


    def send_direct_mail(self):
        template_id = self.env.ref('library_management.library_book_email_template').id
        self.env['mail.template'].browse(template_id).send_mail(self.id,force_send=True)


    def count_state(self):
        good=0
        scrap=0
        for records in self:
            if records.state=="Good Condition":
                good+=1
            elif records.state=="Scrapped":
                scrap+=1
        print("There are ",good,"Books in Good Condition and ",scrap," Books in Scrap Condition.")

        return{
        'type':'ir.actions.client',
        'tag':'display_notification',

        'params':{
        'message':'hiiiiiiiiiiiiiiiiiiiiiiiiiiiiii',
        'type':'success',
        'sticky':False


                    }



             }        

        
        
            # 'message':"You Have {0} Books in Good Contion and {1} Books in Scrap Condition".format(good,scrap),

    def cron_fill_stock(self):
        record=self.env['library.book'].search([])
        for recs in record:
            recs.total_stock+=100
        print("__________self",record)
        print("_______________________100 books added to every books through crone schdeluer")    



              

             



class SaleInfo(models.Model):
    _name = "sale.history.book" #This will be the table name.
    _description = "This Model will store all the sales history of the books"


    book_id=fields.Many2one(comodel_name="library.book",string="Book Name")
    visitor_id=fields.Many2one(comodel_name="visitor.visitor",string="Visitor Name")
    quantity=fields.Integer(string="Quantity")
    price=fields.Float(string="Book Price")
    Subtotal=fields.Float(string="Total Price",compute="cal_price")


    @api.depends('quantity','price')
    def cal_price(self):
        for rec in self:
            rec.Subtotal=0
            rec.Subtotal=rec.quantity*rec.price

    @api.onchange('quantity')        
    def cal_stock(self):
        for rec in self:
            # print("_____________________",rec)
            # print("_____________________",rec.book_id.stock)
            # print("_____________________",rec.quantity)
            # rec.quantity=11111111
            if rec.quantity > rec.book_id.avail_stock:
                rec.quantity=False
                raise ValidationError(_("You cannot Enter Higher Quantity than Available Stock"))

    

    



       


    
    