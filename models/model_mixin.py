# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class ModelMixin(models.AbstractModel):
  _name = 'om_hospital.model.mixin'
  _description = 'Om Hospital Referenced Model'
  _sequence_id = None

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))

  def get_sequence_id(self):
    if not self._sequence_id:
      raise NotImplementedError()

    return self._sequence_id

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          self.get_sequence_id()) or _('New')

    return super(ModelMixin, self).create(vals)

  def write(self, vals):
    if self.reference == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          self.get_sequence_id()) or _('New')

    return super(ModelMixin, self).write(vals)
