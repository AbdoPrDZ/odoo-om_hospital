# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Patient(models.Model):
  _name = 'om_hospital.patient'
  _description = 'Hospital Patient Information'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _rec_name = 'partner_id'
  _order = 'reference desc'

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))
  partner_id = fields.Many2one(
      'res.partner', string='Patient', required=True)
  responsible_id = fields.Many2one(
      'res.partner', string='Responsible')
  age = fields.Integer(string='Age', required=True, tracking=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], required=True, default='male', tracking=True)
  note = fields.Text(string='Description', tracking=True)
  appointments_ids = fields.One2many(
      'om_hospital.appointment', 'patient_id', string="Appointments"
  )
  appointments_count = fields.Integer(
      string="Appointments Count", compute="_compute_appointments_count")
  image = fields.Binary(string="Patient Image",
                        related='partner_id.image_1920', readonly=True)
  # children_ids = fields.One2many(
  #     'res.partner', 'responsible_id', string="Children"
  # )
  children_count = fields.Integer(
      string="Children Count", compute="_compute_children_count")
  active = fields.Boolean(string='Active', default=True, tracking=True)

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

  def name_get(self):
    records = []

    for rec in self:
      records.append((rec.id, rec.partner_id.name if self.env.context.get(
          'hide_ref') else f'[{rec.reference}] {rec.partner_id.name}'))

    return records

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.patient_seq') or _('New')

    vals = self._validate(vals)

    return super(Patient, self).create(vals)

  def write(self, vals):
    for rec in self:
      if rec.reference == _('New'):
        vals['reference'] = self.env['ir.sequence'].next_by_code(
            'om_hospital.patient_seq') or _('New')

      vals = rec._validate(vals)

      super(Patient, rec).write(vals)

  def _compute_appointments_count(self):
    for rec in self:
      if rec.id:
        rec.appointments_count = self.env['om_hospital.appointment'].search_count(
            [('patient_id', '=', rec.id)])

  def _compute_children_count(self):
    for rec in self:
      if rec.id:
        rec.children_count = self.env['om_hospital.patient'].search_count(
            [('responsible_id', '=', rec.partner_id.id)]
        )

  def view_appointments(self):
    domain = [('patient_id', '=', self.id)]

    # Method 1
    # action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]

    # Method 1
    # action = self.env['ir.actions.actions']._for_xml_id(
    #     'om_hospital.action_hospital_appointment')

    # action['domain'] = domain
    # return action

    # Method 1
    return {
        'type': 'ir.actions.act_window',
        'name': 'Appointments',
        'res_model': 'om_hospital.appointment',
        'view_mode': 'tree,form',
        'target': 'current',
        'context': dict({
            'default_patient_id': self.id,
            'hide_patient_id': 1
        }),
        'domain': domain
    }

  def view_children(self):
    return {
        'type': 'ir.actions.act_window',
        'name': 'Children',
        'res_model': 'om_hospital.patient',
        'view_mode': 'tree,form',
        'target': 'current',
        'context': dict({
            'default_responsible_id': self.partner_id.id,
            'hide_responsible_id': 1
        }),
        'domain': [('responsible_id', '=', self.partner_id.id)]
    }
