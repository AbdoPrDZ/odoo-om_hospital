# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Appointment(models.Model):
  _name = 'om_hospital.appointment'
  _description = 'Hospital Appointment Information'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _rec_name = 'patient_id'
  _order = 'reference desc'

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))
  doctor_id = fields.Many2one(
      'om_hospital.doctor', string='Doctor', required=True)
  patient_id = fields.Many2one(
      'om_hospital.patient', string='Patient', required=True)
  age = fields.Integer(string='Age', related='patient_id.age', tracking=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], related='patient_id.gender', tracking=True)
  note = fields.Text(string='Description', tracking=True)
  state = fields.Selection(string='Status', selection=[
      ('draft', 'Draft'),
      ('confirmed', 'Confirmed'),
      ('done', 'Done'),
      ('canceled', 'Canceled'),
  ], required=True, default='draft', tracking=True)
  appointment_date = fields.Date(
      string='Date', required=True, default=fields.Datetime.now)
  checkup_date = fields.Datetime(
      string='Checkup Date', default=fields.Datetime.now)
  prescription_lines_ids = fields.One2many(
      'om_hospital.appointment_prescription_line', 'appointment_id', string='Prescriptions Lines')

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.appointment_seq') or _('New')

    return super(Appointment, self).create(vals)

  def write(self, vals):
    for rec in self:
      if rec.reference == _('New'):
        vals['reference'] = self.env['ir.sequence'].next_by_code(
            'om_hospital.appointment_seq') or _('New')

      super(Appointment, rec).write(vals)

  def action_confirm(self):
    for rec in self:
      rec.state = 'confirmed'

  def action_done(self):
    for rec in self:
      rec.state = 'done'

  def action_cancel(self):
    for rec in self:
      rec.state = 'canceled'

  def action_restore(self):
    for rec in self:
      rec.state = 'draft'
