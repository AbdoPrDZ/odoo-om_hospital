# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Reception(models.Model):
  _name = 'om_hospital.reception'
  _description = "Om Hospital Reception"
  _inherit = ['om_hospital.model.mixin', 'mail.thread', 'mail.activity.mixin']
  _rec_name = 'partner_id'
  _order = 'reference desc'
  _sequence_id = 'om_hospital.reception_seq'

  partner_id = fields.Many2one(
      'res.partner', string='Reception', required=True)
  user_id = fields.Many2one('res.users', string='User',
                            compute='_compute_user_id', store=True, readonly=True)
  age = fields.Integer(string='Age', related='partner_id.age', tracking=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], related='partner_id.gender', tracking=True)
  note = fields.Text(string='Description', tracking=True)
  active = fields.Boolean(string="Active", default=True, tracking=True)
  image = fields.Binary(string="Reception Image",
                        related='partner_id.image_1920', readonly=True)

  def name_get(self):
    records = []

    for rec in self:
      records.append((rec.id, rec.partner_id.name if self.env.context.get(
          'hide_ref') else f'[{rec.reference}] {rec.partner_id.name}'))

    return records

  def _grant_access(self):
    """ Grant access to the reception group for the linked user """
    if self.active:
      if self.partner_id and len(self.partner_id.user_ids) > 0:
        for user in self.partner_id.user_ids:  # Take the first linked user
          reception_group = self.env.ref('om_hospital.group_hospital_reception')

          if reception_group not in user.groups_id:
            reception_group.sudo().write({
                'users': [(4, user.id)]  # Add the user to the reception group
            })
    else:
      self._remove_access()

  def _remove_access(self):
    """ Remove access to the reception group for the linked user """
    if self.partner_id and len(self.partner_id.user_ids) > 0:
      for user in self.partner_id.user_ids:  # Take the first linked user
        reception_group = self.env.ref('om_hospital.group_hospital_reception')

        if reception_group in user.groups_id:
          reception_group.sudo().write({
              'users': [(3, user.id)]  # Remove the user from the reception group
          })

  @api.model
  def create(self, vals):
    """ Override the create method to grant access to the reception group """
    reception = super(Reception, self).create(vals)
    reception._grant_access()
    return reception

  def write(self, vals):
    """ Override the write method to grant access to the reception group """
    for rec in self:
      super(Reception, rec).write(vals)
      rec._grant_access()

  def unlink(self):
    """ Override the unlink method to remove access from the reception group """
    for rec in self:
      rec._remove_access()
      super(Reception, rec).unlink()

  @api.depends('partner_id')
  def _compute_user_id(self):
    for rec in self:
      if rec.partner_id.user_ids:
        rec.user_id = rec.partner_id.user_ids[0].id
      else:
        rec.user_id = False
