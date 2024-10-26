# Copyright 2020 Akretion - Mourad EL HADJ MIMOUNE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    sale_margin = fields.Float(
        default=0,
        digits=(16, 2),
        help="Margin to apply on price to obtain sale price",
    )

    def _get_supplierinfo_pricelist_price(self):
        self.ensure_one()
        sale_price = self.price

        # Aplica el descuento si existe
        if self.discount:
            discount_amount = sale_price * (self.discount / 100)
            sale_price -= discount_amount

        # Aplica el margen de venta si está configurado
        if self.sale_margin:
            sale_price += sale_price * (self.sale_margin / 100)

        return sale_price