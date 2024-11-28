# -- coding: utf-8 --

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'
    
    bs_resource_calendar_leaves = fields.Many2one('resource.calendar.leaves', string='Public Holiday', readonly=True, ondelete='cascade')

    def write(self, vals):
        if self.bs_resource_calendar_leaves and not self.env.context.get('allow_to_change_event'):
            for field in self._get_leaves_readonly_fields():
                if field in vals:
                    raise UserError(_('It is not allowed to modify the dates of a public holiday, please modify it from the public holiday record'))
        return super().write(vals)

    @api.model
    def _get_leaves_readonly_fields(self):
        return [
            'start',
            'stop',
            'duration',
            'start_date',
            'stop_date'
        ]