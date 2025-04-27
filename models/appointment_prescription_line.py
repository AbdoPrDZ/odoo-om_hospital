# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AppointmentPrescriptionLine(models.Model):
  _name = 'om_hospital.appointment_prescription_line'
  _description = 'Hospital Appointment Prescription Line'
  _rec_name = 'medicine_id'

  appointment_id = fields.Many2one(
      'om_hospital.appointment', string="Appointment", required=True, readonly=True)
  medicine_id = fields.Many2one(
      'om_hospital.medicine', string='Medicine', required=True)
  quantity = fields.Integer(string='Quantity', required=True)
  usage = fields.Text(string='Usage Description')

  @api.onchange('medicine_id')
  def _onchange_medicine(self):
    for rec in self:
      if not rec.usage and rec.medicine_id:
        rec.usage = rec.medicine_id.usage
