from odoo import models, fields, api
from datetime import datetime, date


class UpdateEffectiveDate(models.TransientModel):
    _name = "update.effective.date"

    date_done = fields.Datetime(string="Fecha Efectiva")

    def update_date_done(self):
        picking_id = self.env['stock.picking'].browse(self.env.context.get('active_id'))
        if picking_id:
            picking_id.date_done = self.date_done
