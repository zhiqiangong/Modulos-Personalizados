from odoo import models, fields

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    rental_property_id = fields.Many2one('rental.property', string='Rental Property')
    rental_property_address = fields.Char(related='rental_property_id.address', string='Address', readonly=True)
    rental_property_type = fields.Selection(related='rental_property_id.property_type', string='Property Type', readonly=True)
    rental_property_number_of_rooms = fields.Integer(related='rental_property_id.number_of_rooms', string='Number of Rooms', readonly=True)
    rental_property_number_of_bathrooms = fields.Integer(related='rental_property_id.number_of_bathrooms', string='Number of Bathrooms', readonly=True)
    rental_property_size_m2 = fields.Float(related='rental_property_id.size_m2', string='Surface Area (m²)', readonly=True)