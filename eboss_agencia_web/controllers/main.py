from odoo import http
from odoo.http import request
    
class PaginaAlquileres(http.Controller):
    @http.route(['/alquileres'], type='http', auth='public', website=True)
    def alquileres(self, **kw):
        return http.request.render('eboss_agencia_web.alquileres_page')

class PaginaContacto(http.Controller):
    @http.route(['/contacto'], type='http', auth='public', website=True)
    def contacto(self, **kw):
        return http.request.render('eboss_agencia_web.contacto_page')

class PaginaFaqs(http.Controller):
    @http.route(['/faqs'], type='http', auth='public', website=True)
    def faqs(self, **kw):
        return http.request.render('eboss_agencia_web.faqs_page')

class PaginaNosotros(http.Controller):
    @http.route(['/nosotros'], type='http', auth='public', website=True)
    def nosotros(self, **kw):
        return http.request.render('eboss_agencia_web.nosotros_page')
