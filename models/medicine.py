# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Medicine(models.Model):
  _name = 'om_hospital.medicine'
  _description = 'Hospital Medicine Information'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _order = 'reference desc'

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))
  name = fields.Char(string="Name", required=True, tracking=True)
  note = fields.Text(string='Description', tracking=True)
  usage = fields.Text(string='Usage', tracking=True)
  image = fields.Binary(string="Doctor Image")
  active = fields.Boolean(string='Active', default=True, tracking=True)

  def name_get(self):
    records = []

    for rec in self:
      records.append((rec.id, rec.name if self.env.context.get(
          'hide_ref') else f'[{rec.reference}] {rec.name}'))

    return records


  # TODO: Fix duplicate check
  ##############################################################################################################################
  # @api.constrains('name')
  # def check_name(self):
  #   founds = self.env['om_hospital.medicine'].search(
  #       [('name', '=', self.name)])
  #   if founds:
  #     raise models.ValidationError(
  #         _('This medicine "%s" name already exists.', self.name))

  def _validate(self, vals, skip=None):
    if self.env['om_hospital.medicine'].search_count([('name', '=', vals.get('name'))] + [('id', '!=', skip)] if skip else []):
      raise models.ValidationError(
          _('This medicine "%s" name already exists.', vals.get('name')))
  ##############################################################################################################################

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.medicine_seq') or _('New')

    for rec in self:
      rec._validate(vals)

    return super(Medicine, self).create(vals)

  def write(self, vals):
    for rec in self:
      if rec.reference == _('New'):
        vals['reference'] = self.env['ir.sequence'].next_by_code(
            'om_hospital.medicine_seq') or _('New')

      rec._validate(vals, rec.id)

      super(Medicine, rec).write(vals)

  def copy(self, default=None):
    default = default or {}
    if not default.get('name'):
      default['name'] = _('%s (Copy)', self.name)
    default['note'] = _('Copy from %s', self.name)
    return super(Medicine, self).copy(default)
