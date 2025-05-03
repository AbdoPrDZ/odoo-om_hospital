# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Doctor(models.Model):
  _name = 'om_hospital.doctor'
  _description = 'Hospital Doctor Information'
  _inherit = ['om_hospital.model.mixin', 'mail.thread', 'mail.activity.mixin']
  _rec_name = 'partner_id'
  _order = 'reference desc'
  _sequence_id = 'om_hospital.doctor_seq'

  partner_id = fields.Many2one(
      'res.partner', string='Doctor', required=True)
  user_id = fields.Many2one('res.users', string='User',
                            compute='_compute_user_id', store=True, readonly=True)
  age = fields.Integer(string='Age', related='partner_id.age', tracking=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], related='partner_id.gender', store=True, tracking=True)
  note = fields.Text(string='Description', tracking=True)
  appointments_count = fields.Integer(
      string="Appointments Count", compute="_compute_appointments_count")
  active = fields.Boolean(string="Active", default=True, tracking=True)
  image = fields.Binary(string="Doctor Image", related='partner_id.image_1920')
  work_days = fields.Text(string='Work Days', default='[]', tracking=True)

  def name_get(self):
    records = []

    for rec in self:
      records.append((rec.id, rec.partner_id.name if self.env.context.get(
          'hide_ref') else f'[{rec.reference}] {rec.partner_id.name}'))

    return records

  def _grant_access(self):
    """ Grant access to the doctor group for the linked user """
    if self.active:
      if self.partner_id and len(self.partner_id.user_ids) > 0:
        for user in self.partner_id.user_ids:  # Take the first linked user
          doctor_group = self.env.ref('om_hospital.group_hospital_doctor')

          if doctor_group not in user.groups_id:
            doctor_group.sudo().write({
                'users': [(4, user.id)]  # Add the user to the doctor group
            })
    else:
      self._remove_access()

  def _remove_access(self):
    """ Remove access to the doctor group for the linked user """
    if self.partner_id and len(self.partner_id.user_ids) > 0:
      for user in self.partner_id.user_ids:  # Take the first linked user
        doctor_group = self.env.ref('om_hospital.group_hospital_doctor')

        if doctor_group in user.groups_id:
          doctor_group.sudo().write({
              'users': [(3, user.id)]  # Remove the user from the doctor group
          })

  @api.model
  def create(self, vals):
    """ Override the create method to grant access to the doctor group """
    doctor = super(Doctor, self).create(vals)
    doctor._grant_access()
    return doctor

  def write(self, vals):
    """ Override the write method to grant access to the doctor group """
    for rec in self:
      super(Doctor, rec).write(vals)
      rec._grant_access()

  def unlink(self):
    """ Override the unlink method to remove access from the doctor group """
    for rec in self:
      rec._remove_access()
      super(Doctor, rec).unlink()

  @api.depends('partner_id')
  def _compute_user_id(self):
    """ Compute the user_id based on the partner_id """
    for rec in self:
      if rec.partner_id.user_ids:
        rec.user_id = rec.partner_id.user_ids[0].id
      else:
        rec.user_id = False

  def _compute_appointments_count(self):
    """ Compute the appointments count for each doctor """
    for rec in self:
      if rec.id:
        rec.appointments_count = self.env['om_hospital.appointment'].search_count(
            [('doctor_id', '=', rec.id)])

  def view_appointments(self):
    """ View the appointments for the doctor """
    return {
        'type': 'ir.actions.act_window',
        'name': 'Appointments',
        'res_model': 'om_hospital.appointment',
        'view_mode': 'tree,form',
        'target': 'current',
        'context': dict({
            'default_doctor_id': self.id,
            'hide_doctor_id': 1
        }),
        'domain': [('doctor_id', '=', self.id)]
    }
