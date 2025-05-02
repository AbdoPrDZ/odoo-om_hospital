# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons.base.models.res_users import check_identity


class Appointment(models.Model):
  _name = 'om_hospital.appointment'
  _description = 'Hospital Appointment Information'
  _inherit = ['om_hospital.model.mixin', 'mail.thread', 'mail.activity.mixin']
  _rec_name = 'patient_id'
  _order = 'reference desc'
  _sequence_id = 'om_hospital.appointment_seq'

  doctor_id = fields.Many2one(
      'om_hospital.doctor', string='Doctor', required=True, tracking=True)
  patient_id = fields.Many2one(
      'om_hospital.patient', string='Patient', required=True)
  age = fields.Integer(string='Age', compute='_compute_age', store=True, tracking=True)
  gender = fields.Char(string='Gender', compute='_compute_gender', store=True, tracking=True)
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
      string='Checkup Date', tracking=True)
  prescription_lines_ids = fields.One2many(
      'om_hospital.appointment_prescription_line', 'appointment_id', string='Prescriptions Lines')
  amount = fields.Float(string="Amount", required=True, tracking=True)
  active = fields.Boolean(string='Active', default=True, tracking=True)

  def name_get(self):
    """ Override the name_get method to display the reference and patient name """
    records = []

    for rec in self:
      records.append((rec.id, rec.patient_id.partner_id.name if self.env.context.get(
          'hide_ref') else f'[{rec.reference}] {rec.patient_id.partner_id.name}'))

    return records

  @api.depends('patient_id')
  def _compute_age(self):
    """ Compute the age of the patient """
    for rec in self:
      rec.age = rec.patient_id.age if rec.patient_id else 0
    
  @api.depends('patient_id')
  def _compute_gender(self):
    """ Compute the gender of the patient """
    for rec in self:
      rec.gender = rec.patient_id.gender if rec.patient_id else 'male'

  def _current_user_doctor(self):
    """ Get the current user's doctor record """
    
    doctor = False
    if self.env.user.has_group('om_hospital.group_hospital_doctor'):
      doctor = self.env['om_hospital.doctor'].search(
          [('user_id', '=', self.env.user.id)], limit=1)
    
    return doctor

  @api.model
  def default_get(self, vals):
    """ Override the default_get method to set the default values """
    res = super().default_get(vals)

    doctor = self._current_user_doctor()
    if doctor:
      res['doctor_id'] = doctor.id
    
    return res

  @api.depends('doctor_id')
  def check_doctor_id(self):
    """ Check if the current user is a doctor and set the doctor_id accordingly """
    doctor = self._current_user_doctor()
    for rec in self:
      if rec.doctor_id and rec.doctor_id.id != doctor.id:
        raise models.ValidationError(
            'You can\'t modify this appointment.')

  @api.constrains('amount')
  def check_amount(self):
    """ Check if the amount is greater than 0 """
    for rec in self:
      if rec.amount <= 0:
        raise models.ValidationError('Amount must be greater then 0.')

  def only_doctor(self):
    """ Check if the current user is a doctor and raise an error if not """
    if not self._current_user_doctor():
      raise models.ValidationError(
          'You can\'t modify this appointment.')

  @api.constrains('prescription_lines_ids')
  def check_prescription_lines(self):
    """ Check if the prescription lines are empty and set the state accordingly """
    for rec in self:
      if len(rec.prescription_lines_ids) > 0:
        self.only_doctor()
        if rec.state == 'draft':
          rec.state = 'confirm'
      if rec.state == 'confirm' and len(rec.prescription_lines_ids) == 0:
        rec.state = 'draft'

  @api.constrains('checkup_date')
  def check_checkup_date(self):
    """ Check if the checkup date is greater than the current date and allow only doctors to modify it """
    self.only_doctor()

    for rec in self:
      if rec.checkup_date and rec.checkup_date < fields.Datetime.now():
        raise models.ValidationError(
            'Checkup date must be greater than current date.')

  def unlink(self):
    """ Override the unlink method to check the state before deleting """
    for rec in self:
      if not rec.state in ['draft', 'cancel']:
        raise models.ValidationError(
            'You can\'t delete this appointment you have to cancel it first or move it to draft?')
      super(Appointment, rec).unlink()

  def action_confirm(self):
    """ Confirm the appointment """
    for rec in self:
      rec.state = 'confirm'

  def action_done(self):
    """ Mark the appointment as done only if the user is a doctor """
    self.only_doctor()
    for rec in self:
      rec.state = 'done'

  @check_identity
  def action_cancel(self):
    """ Cancel the appointment """
    for rec in self:
      rec.state = 'cancel'

  def action_restore(self):
    """ Restore the appointment to draft state """
    for rec in self:
      rec.state = 'draft'

  def action_url(self):
    """ Open the appointment detail view in a new tab """
    return {
        'type': 'ir.actions.act_url',
        'target': 'new',
        'url': '/om_hospital/appointment/%s' % self.id,
    }
