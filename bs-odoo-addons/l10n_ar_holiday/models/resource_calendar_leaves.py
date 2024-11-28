# -- coding: utf-8 --

from odoo import models, fields, api


class ResourceCalendarLeaves(models.Model):   
    _inherit = 'resource.calendar.leaves'
    
    bs_calendar_event = fields.Many2one('calendar.event', string='Calendar Event')

    @api.model_create_multi
    def create(self, vals_list):
        leaves = super(ResourceCalendarLeaves, self).create(vals_list)
        
        for leave in leaves:
            if not leave.holiday_id or not leave.holiday_id.id:
                event = self.env['calendar.event'].create({
                    'name': 'Feriado - ' + leave.name,
                    'start': leave.date_from,
                    'stop': leave.date_to,
                    'bs_resource_calendar_leaves': leave.id,
                })
                leave.bs_calendar_event = event
    
        return leaves
    
    def write(self, vals):
        # OVERRIDE
        leave = super(ResourceCalendarLeaves, self).write(vals)
        if not self.holiday_id or not self.holiday_id.id:
            event = self.bs_calendar_event
            if event:
                val_to_update = {}
                if 'name' in vals:
                    val_to_update['name'] = 'Feriado - ' + self.name
                if 'date_from' in vals:
                    val_to_update['start'] = self.date_from
                if 'date_to' in vals:
                    val_to_update['stop'] = self.date_to
                if val_to_update:
                    event.with_context(allow_to_change_event=True).write(val_to_update)
        return leave
    
    
    
    
    
    