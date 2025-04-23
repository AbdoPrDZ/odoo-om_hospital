# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Patient(models.Model):
  _name = 'om_hospital.patient'
  _description = 'Hospital Patient Information'
  _inherit = ['mail.thread', 'mail.activity.mixin']

  name = fields.Char(string='Patient Name', required=True)
  age = fields.Integer(string='Age', required=True, default=18)
  gender = fields.Selection(string='Gender', selection=[
      ('male', 'Male'),
      ('female', 'Female'),
  ], required=True, default='male')
  note = fields.Text(string='Medical History')
  state = fields.Selection(string='Status', selection=[
      ('draft', 'Draft'),
      ('confirmed', 'Confirmed'),
      ('done', 'Done'),
      ('canceled', 'Canceled'),
  ], required=True, default='draft')
