# -*- coding: utf-8 -*-

from odoo import models, fields, api

class mlm_product(models.Model):
    _name = 'mlm_product'
    _rec_name = 'default_code'
    _description = "Markets Ids Products"

    default_code = fields.Char('SKU')
    marketplace = fields.Selection([('mercado_libre', 'Mercado Libre'), ('amazon', 'Amazon'),('linio', 'Linio'), ('walmart','Walmart'),('claroshop','ClaroShop'),('elektra','Elektra'),('liverpool','Liverpool'),('somos_reyes_shop','Somos Reyes Shop')],'Marketplace')
    market_identificator = fields.Char("Id Marketplace")
    account_indentificator = fields.Char("Cuenta Marketplace")

#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100