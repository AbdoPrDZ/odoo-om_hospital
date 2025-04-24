# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Patient(models.Model):
  _name = 'om_hospital.patient'
  _description = 'Hospital Patient Information'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _rec_name = 'partner_id'

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))
  partner_id = fields.Many2one(
      'res.partner', string='Patient', required=True)
  responsible_id = fields.Many2one(
      'res.partner', string='Respomsible')
  age = fields.Integer(string='Age', required=True, default=24, tracking=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], required=True, default='male', tracking=True)
  note = fields.Text(string='Description', tracking=True)
  state = fields.Selection(string='Status', selection=[
      ('draft', 'Draft'),
      ('confirmed', 'Confirmed'),
      ('done', 'Done'),
      ('canceled', 'Canceled'),
  ], required=True, default='draft', tracking=True)
  appointments_count = fields.Integer(
      string="Appointments Count", compute="_compute_appointments_count")

  def _validate(self, vals):
    if 'partner_id' in vals and 'responsible_id' in vals and vals['partner_id'] == vals['responsible_id']:
      raise models.ValidationError(
          'The patient and responsible cannot be the same person.')
    if 'age' in vals and vals['age'] < 0:
      raise models.ValidationError(
          'Age cannot be negative. Please enter a valid age.')
    if 'age' in vals and vals['age'] <= 13 and not (vals.get('responsible_id') or self.responsible_id):
      raise models.ValidationError(
          'You must select a responsible for patients under 13 years old.')
    return vals

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.patient_seq') or _('New')

    vals = self._validate(vals)

    return super(Patient, self).create(vals)

  def write(self, vals):
    if self.reference == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.patient_seq') or _('New')

    vals = self._validate(vals)

    return super(Patient, self).write(vals)

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

  def _compute_appointments_count(self):
    for rec in self:
      if rec.id:
        rec.appointments_count = self.env['om_hospital.appointment'].search_count(
            [('patient_id', '=', rec.id)])
