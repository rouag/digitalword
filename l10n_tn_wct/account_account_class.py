# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO, Open Source Management Solution
#    Copyright (C) 2017 Digital Word
#
##############################################################################

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp


class AccountAccountClassTemplate(models.Model):
    _inherit = "account.account.template"



   # parent_id = fields.Integer("Parent ")
    code_secondaire = fields.Char("code secondaire")


   # @api.one
   # @api.depends('code')
   # def _compute_display_name(self):
       # code_secondaire = self.code
       # self.code_id = code_secondaire


class AccountResPartner(models.Model):
    _inherit = "res.partner"

    num_fiscal = fields.Char("Numéro fiscal")