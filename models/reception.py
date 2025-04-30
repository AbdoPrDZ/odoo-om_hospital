# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Reception(models.Model):
  _name = 'om_hospital.reception'
  _description = "Om Hospital Reception"
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _rec_name = 'partner_id'
  _order = 'reference desc'

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))
  partner_id = fields.Many2one(
      'res.partner', string='Reception', required=True)
  user_id = fields.Many2one('res.users', string='User',
                            compute='_compute_user_id', store=True, readonly=True)
  age = fields.Integer(string='Age', required=True, tracking=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], required=True, default='male', tracking=True)
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
    if self.partner_id and len(self.partner_id.user_ids) > 0:
      for user in self.partner_id.user_ids:  # Take the first linked user
        reception_group = self.env.ref('om_hospital.group_hospital_reception')

        if reception_group not in user.groups_id:
          reception_group.sudo().write({
              'users': [(4, user.id)]  # Add the user to the reception group
          })

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.reception_seq') or _('New')

    reception = super(Reception, self).create(vals)
    reception._grant_access()
    return reception

  def write(self, vals):
    for rec in self:
      if rec.reference == _('New'):
        vals['reference'] = self.env['ir.sequence'].next_by_code(
            'om_hospital.reception_seq') or _('New')
      super(Reception, rec).write(vals)
      rec._grant_access()

  def unlink(self):
    for rec in self:
      # Check if the reception is linked to a user and remove the access
      if rec.partner_id and len(rec.partner_id.user_ids) > 0:
        for user in rec.partner_id.user_ids:
          reception_group = self.env.ref(
              'om_hospital.group_hospital_reception')
          if reception_group in user.groups_id:
            reception_group.sudo().write({
                # Remove the user from the reception group
                'users': [(3, user.id)]
            })
      super(Reception, rec).unlink()

  @api.depends('partner_id')
  def _compute_user_id(self):
    for rec in self:
      if rec.partner_id.user_ids:
        rec.user_id = rec.partner_id.user_ids[0].id
      else:
        rec.user_id = False
