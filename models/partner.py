# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Partner(models.Model):
  _inherit = 'res.partner'

  age = fields.Integer(string='Age', required=True)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], required=True, default='male')
  is_reception = fields.Boolean(
      string='Is Reception', compute="_is_reception_compute", store=True, readonly=True)
  is_doctor = fields.Boolean(
      string='Is Doctor', compute="_is_doctor_compute", store=True, readonly=True)
  is_patient = fields.Boolean(
      string='Is Patient', compute="_is_patient_compute", store=True, readonly=True)

  def check_age(self):
    """ Check if the age is valid """
    for rec in self:
      if rec.age < 0 or rec.age > 180:
        raise ValueError("Age must be between 0 and 180")

  def _is_reception_compute(self):
    for rec in self:
      rec.is_reception = self.env['om_hospital.reception'].search_count(
          [('partner_id', '=', rec.id)]) > 0

  def _is_doctor_compute(self):
    for rec in self:
      rec.is_doctor = self.env['om_hospital.doctor'].search_count(
          [('partner_id', '=', rec.id)]) > 0

  def _is_patient_compute(self):
    for rec in self:
      rec.is_patient = self.env['om_hospital.patient'].search_count(
          [('partner_id', '=', rec.id)]) > 0
