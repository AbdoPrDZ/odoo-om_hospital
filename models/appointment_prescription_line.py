# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AppointmentPrescriptionLine(models.Model):
  _name = 'om_hospital.appointment_prescription_line'
  _description = 'Hospital Appointment Prescription Line'
  _rec_name = 'medicine_id'

  appointment_id = fields.Many2one(
      'om_hospital.appointment', string="Appointment", readonly=True)
  medicine_id = fields.Many2one(
      'om_hospital.medicine', string='Medicine', required=True)
  quantity = fields.Integer(string='Quantity', required=True)
  usage = fields.Text(string='Usage Description')
  active = fields.Boolean(string='Active', default=True)

  def name_get(self):
    return [(rec.id, f'[{rec.medicine_id.reference}] {rec.medicine_id.name}') for rec in self]

  @api.onchange('medicine_id')
  def _onchange_medicine(self):
    for rec in self:
      if not rec.usage and rec.medicine_id:
        rec.usage = rec.medicine_id.usage
