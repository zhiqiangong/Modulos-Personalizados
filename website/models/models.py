from odoo import models, fields

class Alquiler(models.Model):
    _name = 'pagina_alquileres.alquiler'
    _description = 'Propiedades en Alquiler'

    name = fields.Char('Nombre de la Propiedad', required=True)
    description = fields.Text('Descripción')
    price = fields.Float('Precio de Alquiler')
    location = fields.Char('Ubicación')
    image = fields.Binary('Imagen')
