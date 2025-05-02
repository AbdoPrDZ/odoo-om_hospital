# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Patient(models.Model):
  _name = 'om_hospital.patient'
  _description = 'Hospital Patient Information'
  _inherit = ['om_hospital.model.mixin', 'mail.thread', 'mail.activity.mixin']
  _rec_name = 'partner_id'
  _order = 'reference desc'
  _sequence_id = 'om_hospital.patient_seq'

  partner_id = fields.Many2one(
      'res.partner', string='Patient', required=True)
  responsible_id = fields.Many2one(
      'res.partner', string='Responsible')
  age = fields.Integer(string='Age', related='partner_id.age', tracking=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], related='partner_id.gender', tracking=True)
  note = fields.Text(string='Description', tracking=True)
  appointments_ids = fields.One2many(
      'om_hospital.appointment', 'patient_id', string="Appointments"
  )
  appointments_count = fields.Integer(
      string="Appointments Count", compute="_compute_appointments_count")
  image = fields.Binary(string="Patient Image",
                        related='partner_id.image_1920', readonly=True)
  children_count = fields.Integer(
      string="Children Count", compute="_compute_children_count")
  active = fields.Boolean(string='Active', default=True, tracking=True)

  def _validate(self, vals):
    if 'partner_id' in vals and 'responsible_id' in vals and vals['partner_id'] == vals['responsible_id']:
      raise models.ValidationError(
          'The patient and responsible cannot be the same person.')
    if 'partner_id' in vals and vals['partner_id']:
      partner = self.env['res.partner'].browse(vals['partner_id'])
      if partner.age and partner.age < 13 and 'responsible_id' not in vals:
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
    vals = self._validate(vals)

    return super(Patient, self).create(vals)

  def write(self, vals):
    for rec in self:
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
