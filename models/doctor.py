# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Doctor(models.Model):
  _name = 'om_hospital.doctor'
  _description = 'Hospital Doctor Information'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _rec_name = 'partner_id'
  _order = 'reference desc'

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))
  partner_id = fields.Many2one(
      'res.partner', string='Doctor', required=True)
  age = fields.Integer(string='Age', required=True, tracking=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], required=True, default='male', tracking=True)
  note = fields.Text(string='Description', tracking=True)
  appointments_count = fields.Integer(
      string="Appointments Count", compute="_compute_appointments_count")
  active = fields.Boolean(string="Active", default=True)
  image = fields.Binary(string="Doctor Image")

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.doctor_seq') or _('New')

    return super(Doctor, self).create(vals)

  def write(self, vals):
    for rec in self:
      if rec.reference == _('New'):
        vals['reference'] = self.env['ir.sequence'].next_by_code(
            'om_hospital.doctor_seq') or _('New')
      super(Doctor, rec).write(vals)

  def _compute_appointments_count(self):
    for rec in self:
      if rec.id:
        rec.appointments_count = self.env['om_hospital.appointment'].search_count(
            [('doctor_id', '=', rec.id)])

  def view_appointments(self):
    return {
        'type': 'ir.actions.act_window',
        'name': 'Appointments',
        'res_model': 'om_hospital.appointment',
        'view_mode': 'tree,form',
        'target': 'current',
        'target': 'current',
        'context': dict({}),
        'domain': [('doctor_id', '=', self.id)]
    }
