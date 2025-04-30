# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.base.models.res_users import check_identity


class Appointment(models.Model):
  _name = 'om_hospital.appointment'
  _description = 'Hospital Appointment Information'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _rec_name = 'patient_id'
  _order = 'reference desc'

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))
  doctor_id = fields.Many2one(
      'om_hospital.doctor', string='Doctor', required=True, tracking=True, readonly=True)
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
      ('confirm', 'Confirm'),
      ('done', 'Done'),
      ('cancel', 'Cancel'),
  ], required=True, default='draft', tracking=True)
  appointment_date = fields.Date(
      string='Date', required=True, default=fields.Datetime.now, tracking=True)
  checkup_date = fields.Datetime(
      string='Checkup Date', default=fields.Datetime.now, tracking=True)
  prescription_lines_ids = fields.One2many(
      'om_hospital.appointment_prescription_line', 'appointment_id', string='Prescriptions Lines')
  amount = fields.Float(string="Amount", required=True, tracking=True)
  active = fields.Boolean(string='Active', default=True, tracking=True)

  def name_get(self):
    records = []

    for rec in self:
      records.append((rec.id, rec.patient_id.partner_id.name if self.env.context.get(
          'hide_ref') else f'[{rec.reference}] {rec.patient_id.partner_id.name}'))

    return records

  @api.model
  def default_get(self, fields):
    res = super().default_get(fields)
    doctor = self.env['om_hospital.doctor'].search(
        [('user_id', '=', self.env.user.id)], limit=1)
    if doctor:
      res['doctor_id'] = doctor.id
    return res

  @api.constrains('amount')
  def check_amount(self):
    for rec in self:
      if rec.amount <= 0:
        raise models.ValidationError('Amount must be greater then 0.')

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

  def unlink(self):
    for rec in self:
      if not rec.state in ['draft', 'cancel']:
        raise models.ValidationError(
            'You can\'t delete this appointment you have to cancel it first or move it to draft?')
      super(Appointment, rec).unlink()

  def action_confirm(self):
    for rec in self:
      rec.state = 'confirm'

  def action_done(self):
    for rec in self:
      rec.state = 'done'

  @check_identity
  def action_cancel(self):
    for rec in self:
      rec.state = 'cancel'

  def action_restore(self):
    for rec in self:
      rec.state = 'draft'

  def action_url(self):
    return {
        'type': 'ir.actions.act_url',
        'target': 'new',
        'url': 'https://github.com/AbdoPrDZ/odoo-om_hospital'
    }
