from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    rental_property_id = fields.Many2one('rental.property', string='Rental Property')

    @api.constrains('start', 'stop', 'rental_property_id')
    def _check_overlapping_appointments(self):
        for event in self:
            if event.rental_property_id:
                overlapping_events = self.search([
                    ('rental_property_id', '=', event.rental_property_id.id),
                    ('id', '!=', event.id),
                    ('start', '<', event.stop),
                    ('stop', '>', event.start),
                ])
                if overlapping_events:
                    raise ValidationError("This property is already booked for the selected time interval.")