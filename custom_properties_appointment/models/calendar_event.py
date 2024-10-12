from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    rental_property_id = fields.Many2one('rental.property', string='Rental Property')

    @api.constrains('start', 'stop', 'rental_property_id')
    def _check_event_overlap(self):
        for event in self:
            overlapping_events = self.search([
                ('id', '!=', event.id),
                ('rental_property_id', '=', event.rental_property_id.id),
                ('start', '<', event.stop),
                ('stop', '>', event.start),
            ])
            if overlapping_events:
                raise ValidationError("You cannot have overlapping events for the same rental property.")

    @api.model
    def check_event_conflict(self, event_id, start, stop, rental_property_id):
        overlapping_events = self.search([
            ('id', '!=', event_id),
            ('rental_property_id', '=', rental_property_id),
            ('start', '<', stop),
            ('stop', '>', start),
        ])
        return {'conflict': bool(overlapping_events)}