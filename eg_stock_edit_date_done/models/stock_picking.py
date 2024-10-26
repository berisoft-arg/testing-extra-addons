from odoo import models, fields, api, _

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def update_date_done(self):
        return {
            'name': "Update Effective Date",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'update.effective.date',
            'target': 'new',
        }