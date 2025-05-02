# -*- coding: utf-8 -*-

import base64
import io

from odoo import models


class AppointmentReportXlsx(models.AbstractModel):
  _name = 'report.om_hospital.appointment_report_xlsx'
  _inherit = 'report.report_xlsx.abstract'

  @property
  def _date_format(self):
    lang = self.env['res.lang'].search([('code', '=', self.env.context['lang'])])
    return lang.date_format

  def generate_xlsx_report(self, workbook, data, appointments):
    sheet = workbook.add_worksheet('Appointments')
    header_format = workbook.add_format(
        {'bold': True, 'align': 'center', 'bg_color': '#00AEAC', 'font_color': '#09406B'})

    j = 0
    for col in ['Image', 'ID', 'Reference', 'Patient', 'Doctor', 'Age', 'Gender', 'Description', 'State', 'Date', 'Checkup Date', 'Amount']:
      sheet.write(0, j, col, header_format)
      j += 1

    sheet.set_column('A:A', 20)  # Image
    sheet.set_column('B:B', 8)   # ID
    sheet.set_column('C:C', 18)  # Reference
    sheet.set_column('D:D', 30)  # Patient
    sheet.set_column('E:E', 30)  # Doctor
    sheet.set_column('F:F', 8)   # Age
    sheet.set_column('G:G', 12)  # Gender
    sheet.set_column('H:H', 40)  # Description
    sheet.set_column('I:I', 15)  # State
    sheet.set_column('J:J', 18)  # Date
    sheet.set_column('K:K', 18)  # Checkup Date
    sheet.set_column('L:L', 15)  # Amount

    i = 1
    for appointment in appointments:
      if appointment.patient_id.image:
        appointment_image = io.BytesIO(base64.b64decode(appointment.patient_id.image))
        sheet.insert_image(i, 0, "image.png", {'image_data':
                           appointment_image, 'x_scale': 0.1, 'y_scale': 0.1})
      sheet.write(i, 1, appointment.id)
      sheet.write(i, 2, appointment.reference)
      sheet.write(i, 3, appointment.patient_id.partner_id.name)
      sheet.write(i, 4, appointment.doctor_id.partner_id.name)
      sheet.write(i, 5, appointment.age)
      sheet.write(i, 6, appointment.gender)
      if appointment.note:
        sheet.write(i, 7, appointment.note)
      sheet.write(i, 8, appointment.state)
      if appointment.appointment_date:
        sheet.write(i, 9, appointment.appointment_date.strftime(self._date_format))
      if appointment.checkup_date:
        sheet.write(i, 10, appointment.checkup_date.strftime(self._date_format))
      sheet.write(i, 11, appointment.amount)
      i += 1

    footer_format = workbook.add_format({'bold': True, 'align': 'right', 'bg_color': '#D3D3D3'})

    if 'date_range' in data:
      date_from, date_to = data['date_range']
      sheet.write(i, 10, 'Date From', footer_format)
      sheet.write(i, 11, date_from, footer_format)
      i += 1
      sheet.write(i, 10, 'Date To', footer_format)
      sheet.write(i, 11, date_to, footer_format)
      i += 1

    # Add a footer row for the total amount
    total_amount = sum(appointment.amount for appointment in appointments)
    sheet.write(i, 10, 'Total', footer_format)
    sheet.write(i, 11, total_amount, footer_format)
