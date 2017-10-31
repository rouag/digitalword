# -*- encoding: utf-8 -*-

{
    'name' : 'Digital word Report',
    'version' : '1.0',
    'author' : 'DigitWord  ERP',
    'website': 'http://www.digitwrod.com',
    'summary': 'Theme digital word in Tunisia with odoo 10',
    'category' : 'theme/Account Charts',
    'description': """
This is the base module to manage Chart of theme and Taxes template for companies in Tunisia.
=================================================================================================
Ce Module charge le modèle du plan de comptes standard Tunisien et permet de générer les états
comptables aux normes tunisiennes.""",

    'depends': [],
    'init_xml' : [],
    'data': [

       # 'account_account_template_view.xml',
        'report_format_header.xml',
        'report_saleorder_document_adress.xml',
    ],
  'images': [
		'images/logo.png',
        ],
    'test': [],
    'demo_xml' : [],
    'active': True,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
