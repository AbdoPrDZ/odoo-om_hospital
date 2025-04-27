# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Medicine(models.Model):
  _name = 'om_hospital.medicine'
  _description = 'Hospital Medicine Information'
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _order = 'reference desc'

  reference = fields.Char(string='Reference', required=True, copy=False, readonly=True,
                          default=lambda self: _('New'))
  name = fields.Char(string="Name", required=True)
  note = fields.Text(string='Description')
  usage = fields.Text(string='Usage')
  image = fields.Binary(string="Doctor Image")

  @api.model
  def create(self, vals):
    if vals.get('reference', ('New')) == _('New'):
      vals['reference'] = self.env['ir.sequence'].next_by_code(
          'om_hospital.medicine_seq') or _('New')

    return super(Medicine, self).create(vals)

  def write(self, vals):
    for rec in self:
      if rec.reference == _('New'):
        vals['reference'] = self.env['ir.sequence'].next_by_code(
            'om_hospital.medicine_seq') or _('New')
      super(Medicine, rec).write(vals)
