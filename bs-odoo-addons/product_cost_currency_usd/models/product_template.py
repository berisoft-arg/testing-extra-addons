from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Nuevo campo de selección para controlar moneda y costo
    currency_selection = fields.Selection(
        selection=[('ARS', 'ARS'), ('USD', 'USD')],
        string="Moneda",
        default='ARS',
        required=True
    )
    currency_id = fields.Many2one('res.currency', string='Divisa', compute='_compute_currency_and_cost', store=True)
    cost_currency_id = fields.Many2one('res.currency', string='Divisa del Costo', compute='_compute_currency_and_cost', store=True)

    @api.depends('currency_selection')
    def _compute_currency_and_cost(self):
        """
        Ajusta las divisas basándose en la selección de moneda.
        """
        currency_map = {
            'ARS': 'base.ARS',  # Reemplaza con el XML ID real de ARS en tu base de datos
            'USD': 'base.USD',  # Reemplaza con el XML ID real de USD en tu base de datos
        }
        for product in self:
            currency_ref = currency_map.get(product.currency_selection)
            if currency_ref:
                currency = self.env.ref(currency_ref)
                product.currency_id = currency
                product.cost_currency_id = currency
