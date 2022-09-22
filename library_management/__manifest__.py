{
    'name' : 'Library Managment',
    'version' : '1.0',
    'sequence': -200,
    'description': "This is an Library Managment Module",
    #'images' : ['images/accounts.jpeg','images/bank_statement.jpeg','images/cash_register.jpeg','images/chart_of_accounts.jpeg','images/customer_invoice.jpeg','images/journal_entries.jpeg'],
    'depends' : ['mail','sale','contacts'],
    'data': ['security/ir.model.access.csv',
    'data/mail_template.xml',
    'data/server_actions_data.xml',
    'data/crons_data.xml',
    'views/visitors.xml',
    'views/librarian.xml',
    'views/library_management.xml',
    'views/library_book.xml',
    "views/sale_order_views.xml"
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',

}