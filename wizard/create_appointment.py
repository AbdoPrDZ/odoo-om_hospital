# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CreateAppointmentWizard(models.TransientModel):
  _name = 'om_hospital.appointment_wizard'
  _description = 'Create Appointment Wizard'

  patient_id = fields.Many2one(
      'om_hospital.patient', string='Patient', required=True)
  doctor_id = fields.Many2one(
      'om_hospital.doctor', string='Doctor', required=True)
  note = fields.Text(string='Description')

  # @api.model
  # def default_get(self, fields):
  #   res = super(CreateAppointmentWizard, self).default_get(fields)
  #   active_id = self.env.context.get('active_id')
  #   if active_id:
  #     patient = self.env['om_hospital.patient'].browse(active_id)
  #     doctor = self.env['om_hospital.doctor'].browse(active_id)
  #     if patient:
  #       res.update({
  #           'patient_id': patient.id if patient else fields.get('patient_id'),
  #           'doctor_id': doctor.id if doctor else fields.get('doctor_id'),
  #       })
  #   return res

  def create_appointment(self):
    vals = {
        'patient_id': self.patient_id.id,
        'doctor_id': self.doctor_id.id,
        'note': self.note,
    }
    rec = self.env['om_hospital.appointment'].create(vals)
    return {
        'name': _('Appointment'),
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'om_hospital.appointment',
        'res_id': rec.id,
        'context': {
            'default_patient_id': self.patient_id.id,
            'hide_patient_id': 1,
        }
    }

  def view_patient_appointments(self):
    action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
    action['domain'] = [('patient_id', '=', self.patient_id.id)]
    action['context'] = dict({
        'default_patient_id': self.patient_id.id,
        'hide_patient_id': 1,
    })
    return action

  def view_doctor_appointments(self):
    action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
    action['domain'] = [('doctor_id', '=', self.doctor_id.id)]
    action['context'] = dict({
        'default_doctor_id': self.patient_id.id,
        'hide_doctor_id': 1
    })
    return action
