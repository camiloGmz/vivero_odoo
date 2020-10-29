# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class Order(models.Model):
    _name = 'vivero.pedido'
    _description = 'Pedidos'

    plant_id = fields.Many2one('vivero.planta', required=True)
    customer_id = fields.Many2one('vivero.cliente', string="Cliente")
    state = fields.Selection([
        ('borrador', 'Borrador'),
        ('confirmar', 'Confirmado'),
        ('cancelar', 'Cancelado')
    ], default='borrador', group_expand='_expand_states')
    last_modification = fields.Datetime(readonly=True)

    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    def write(self, values):
        values['last_modification'] = fields.Datetime.now()
        return super(Order, self).write(values)

    def unlink(self):
        for order in self:
            if order.state == 'confirmar':
                raise UserError("No puedes eliminar las ordenes confirmadas")
        return super(Order, self).unlink()

    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(
                    force_company = vals['company_id']
                ).next_by_code('planta.pedido') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('planta.pedido') or _('New')
        return super(Order, self).create(vals)

class Plantas(models.Model):
    _name = 'vivero.planta'
    _description = "Plantas"

    name = fields.Char('Nombre de la planta')
    price = fields.Float(string='Precio')
    order_ids = fields.One2many('vivero.pedido', 'plant_id', string='Pedidos')
    order_count = fields.Integer(compute='_compute_order_count', store=True, string='Total vendidos')

    number_in_stock = fields.Integer()

    image = fields.Binary('Foto', attachment=True)

    @api.depends('order_ids')
    def _compute_order_count(self):
        for plant in self:
            plant.order_count = len(plant.order_ids)

    @api.constrains('order_count', 'number_in_stock')
    def _check_available_in_stock(self):
        for plant in self:
            if plant.number_in_stock and plant.order_count > plant.number_in_stock:
                raise UserError('Solo hay %s %s en stock pero %s estan vendidas'
                                % (plant.number_in_stock, plant.name, plant.order_count))


class Customer(models.Model):
    _name = 'vivero.cliente'
    _description = "Clientes"

    name = fields.Char('Nombre del cliente', required = True)
    email = fields.Char(help='Para recibir información')
    mobile = fields.Char('Telefono')
    image = fields.Binary('Foto', attachment=True)
    address = fields.Char('Direccion')
    country_id = fields.Many2one('res.country', string='Pais')
    partner_id = fields.Many2one('res.partner', string='Direccion del cliente')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.image_1920:
                self.image = self.partner_id.image_1920
            if self.partner_id.email:
                self.email = self.partner_id.email
            if self.partner_id.mobile:
                self.mobile = self.partner_id.mobile
            if self.partner_id.country_id:
                self.country_id = self.partner_id.country_id.id
            if not self.address:
                self.address = self.partner_id.with_context(show_address_only=True, address_inline=True)._get_name()
