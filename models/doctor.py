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
  active = fields.Boolean(string="Active", default=True, tracking=True)
  image = fields.Binary(string="Doctor Image",
                        related='partner_id.image_1920', readonly=True)

  def name_get(self):
    records = []

    for rec in self:
      records.append((rec.id, rec.partner_id.name if self.env.context.get(
          'hide_ref') else f'[{rec.reference}] {rec.partner_id.name}'))

    return records

  def _grant_access(self):
    """ Grant access to the doctor group for the linked user """
    if self.partner_id and len(self.partner_id.user_ids) > 0:
      for user in self.partner_id.user_ids:  # Take the first linked user
        doctor_group = self.env.ref('om_hospital.group_hospital_doctor')
        
        if doctor_group not in user.groups_id:
          doctor_group.sudo().write({
              'users': [(4, user.id)]  # Add the user to the doctor group
          })

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.doctor_seq') or _('New')

    doctor = super(Doctor, self).create(vals)
    doctor._grant_access()
    return doctor

  def write(self, vals):
    for rec in self:
      if rec.reference == _('New'):
        vals['reference'] = self.env['ir.sequence'].next_by_code(
            'om_hospital.doctor_seq') or _('New')
      super(Doctor, rec).write(vals)
      rec._grant_access()

  def unlink(self):
    for rec in self:
      # Check if the doctor is linked to a user and remove the access
      if rec.partner_id and len(rec.partner_id.user_ids) > 0:
        for user in rec.partner_id.user_ids:
          doctor_group = self.env.ref('om_hospital.group_hospital_doctor')
          if doctor_group in user.groups_id:
            doctor_group.sudo().write({
                'users': [(3, user.id)]  # Remove the user from the doctor group
            })
      super(Doctor, rec).unlink()

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
        'context': dict({
            'default_doctor_id': self.id,
            'hide_doctor_id': 1
        }),
        'domain': [('doctor_id', '=', self.id)]
    }
