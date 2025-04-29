# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
  _inherit = 'res.partner'

  is_patient = fields.Boolean(string='Is Patient', compute="_is_patient_compute", store=True, readonly=True)
  is_doctor = fields.Boolean(string='Is Doctor', compute="_is_doctor_compute", store=True, readonly=True)

  def _is_patient_compute(self):
    for rec in self:
      rec.is_patient = self.env['om_hospital.patient'].search_count([('partner_id', '=', rec.id)]) > 0

  def _is_doctor_compute(self):
    for rec in self:
      rec.is_doctor = self.env['om_hospital.doctor'].search_count([('partner_id', '=', rec.id)]) > 0
