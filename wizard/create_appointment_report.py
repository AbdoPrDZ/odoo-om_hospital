# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CreateAppointmentReportWizard(models.TransientModel):
  _name = 'om_hospital.appointment_report_wizard'
  _description = 'Create Appointment Report Wizard'

  patient_id = fields.Many2one(
      'om_hospital.patient', string='Patient', required=True)
  date_from = fields.Date(string="From Date", required=True)
  date_to = fields.Date(string="To Date", required=True,
                        default=fields.Datetime.now)
  appointments_count = fields.Integer(
      string='Appointments Count', compute='_appointments_count_compute')

  @api.depends('date_from', 'date_to', 'patient_id')
  def _appointments_count_compute(self):
    for rec in self:
      if rec.date_from and rec.date_to and rec.patient_id:
        count = self.env['om_hospital.appointment'].search_count([
            ('patient_id', '=', rec.patient_id.id),
            ('appointment_date', '>=', rec.date_from),
            ('appointment_date', '<=', rec.date_to)
        ])
        rec.appointments_count = count
      else:
        rec.appointments_count = 0

  def create_appointment_pdf_report(self):
    records = self.env['om_hospital.appointment'].search([
        ('patient_id', '=', self.patient_id.id),
        ('appointment_date', '>=', self.date_from),
        ('appointment_date', '<=', self.date_to)
    ])
    return self.env.ref('om_hospital.report_appointment_details').report_action(records)

  def create_appointment_xlsx_report(self):
    records = self.env['om_hospital.appointment'].search([
        ('patient_id', '=', self.patient_id.id),
        ('appointment_date', '>=', self.date_from),
        ('appointment_date', '<=', self.date_to)
    ])
    data = {'date_range': [self.date_from, self.date_to]}
    return self.env.ref('om_hospital.report_appointment_details_xlsx').report_action(records, data=data)

  def view_patient_appointments(self):
    action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
    action['domain'] = [
        ('patient_id', '=', self.patient_id.id),
        ('appointment_date', '>=', self.date_from),
        ('appointment_date', '<=', self.date_to)
    ]
    action['context'] = dict({
        'default_patient_id': self.patient_id.id,
        'hide_patient_id': 1,
    })
    action['target'] = 'new'
    return action
