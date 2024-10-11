from odoo import fields, models, api


class ModelName(models.TransientModel):
    _name = 'rental.payment.wizard'
    _description = 'Description'

    tenant_id = fields.Many2one('res.partner', string='Tenant')
    payment_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('services', 'Services')
    ], string='Payment Type')
    inmueble = fields.Selection([
        ('Property', 'Property'),
        ('Room', 'Room')
    ], string='Inmueble',default='Property')
    service_ids = fields.One2many(
        "rental.payment.history.lines", "payment_id", string="Service"
    )
    invoice_count = fields.Integer(string="Invoice Count", compute="_compute_invoice_count")

    alquiler_price = fields.Float(string='Precio Alquiler($)', required=True)
    invoice_id = fields.Many2one('account.move', string='Invoice')
    property_id = fields.Many2one('rental.property', string='Property',domain="[('tenant_id', '=', tenant_id)]")
    room_id = fields.Many2one('rental.room', string='Room', domain="[('tenant_id', '=', tenant_id)]")


    @api.depends('tenant_id')
    def _compute_invoice_count(self):
        for record in self:
            partner = record.tenant_id
            if partner:
                record.invoice_count = self.env['account.move'].search_count(
                    [('partner_id', '=', partner.id), ('move_type', '=', 'out_invoice')])
            else:
                record.invoice_count = 0

    def action_create_invoice(self):
        self.ensure_one()
        invoice_lines = []

        if self.payment_type == 'monthly':
            # Agrega un producto de Pago de Alquiler con cantidad 1
            rental_product = self.env['product.product'].search([
                ('name', '=', 'Pago de Alquiler'),
                ('detailed_type', '=', 'service')
            ], limit=1)
            if rental_product:
                invoice_lines.append((0, 0, {
                    'product_id': rental_product.id,
                    'quantity': 1,
                    'price_unit': self.alquiler_price,
                }))
        else:
            for service in self.service_ids:
                account_id = service.product_id.property_account_income_id.id or service.product_id.categ_id.property_account_income_categ_id.id
                invoice_lines.append((0, 0, {
                    'product_id': service.product_id.id,
                    'quantity': service.quantity,
                    'price_unit': service.price,
                    'account_id': account_id,
                }))

        invoice = self.env['account.move'].create({
            'partner_id': self.tenant_id.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_lines,
        })
        invoice.action_post()
        # crear el hito de pago en rental.payment.history
        rental = self.env['rental.payment.history'].create({
            'tenant_id': self.tenant_id.id,
            'payment_type': self.payment_type,
            'inmueble': self.inmueble,
            'invoice_id': invoice.id,
            'property_id': self.property_id.id,
            'room_id': self.room_id.id,
        })
        invoice.write({'payment_history_id': rental.id}) # Relacionar la factura con el hito de pago
        return {
            'type': 'ir.actions.act_window',
            'name': 'Factura Pago de Alquiler',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': invoice.id,
            'target': 'current',  # Abre en la misma ventana
        }


class RentalPaymentHistoryLines(models.TransientModel):
    _name = 'rental.payment.history.lines'
    _description = ' Payment History Lines'

    payment_id = fields.Many2one('rental.payment.wizard', string='Payment')
    product_id = fields.Many2one("product.product", string="Product")
    quantity = fields.Float(string='Quantity')
    price = fields.Float(string='Price')
    observations = fields.Text(string='Observations')
