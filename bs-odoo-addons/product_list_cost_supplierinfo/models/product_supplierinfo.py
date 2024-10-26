# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductSupplierInfo(models.Model):
     _inherit = 'product.supplierinfo'
     

     list_name = fields.Char('Lista de Precios')

     product_cost = fields.Float(
        string="Costo",
        compute="_compute_product_cost",
        store=True,
        help="Cost of the product after applying the supplier discount."
    )

     @api.depends('price', 'discount')
     def _compute_product_cost(self):
        for record in self:
    # Si el descuento es cero, el product_cost será igual a price
            discount = record.discount or 0.0
            record.product_cost = record.price - (record.price * discount / 100.0) 
