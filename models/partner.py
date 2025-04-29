# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
  _inherit = 'res.partner'

  is_patient = fields.Boolean(string='Is Patient', compute="_is_patient_compute")

  def _is_patient_compute(self):
    for rec in self:
        rec.is_patient = self.env['om_hospital.patient'].search_count([('partner_id', '=', rec.id)]) > 0
