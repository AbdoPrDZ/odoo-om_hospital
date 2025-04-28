# -*- coding: utf-8 -*-

import base64
import io

from odoo import models


class PatientReportXlsx(models.AbstractModel):
  _name = 'report.om_hospital.patient_report_xlsx'
  _inherit = 'report.report_xlsx.abstract'

  def generate_xlsx_report(self, workbook, data, patients):
    sheet = workbook.add_worksheet('Patients')
    header_format = workbook.add_format(
        {'bold': True, 'align': 'center', 'bg_color': '#00aeac', 'font_color': '#09406b'})

    j = 0
    for col in ['Image', 'ID', 'Reference', 'Name', 'Responsible', 'Age', 'Gender', 'Description', 'Appointments Count', 'Children Count']:
      sheet.write(0, j, col, header_format)
      j += 1

    sheet.set_column('A:A', 15)  # Image
    sheet.set_column('B:B', 10)  # ID
    sheet.set_column('C:C', 15)  # Reference
    sheet.set_column('D:D', 25)  # Name
    sheet.set_column('E:E', 25)  # Responsible
    sheet.set_column('F:F', 10)  # Age
    sheet.set_column('G:G', 10)  # Gender
    sheet.set_column('H:H', 35)  # Description
    sheet.set_column('I:I', 20)  # Appointments Count
    sheet.set_column('J:J', 20)  # Children Count

    i = 1
    for patient in patients:
      if patient.image:
        patient_image = io.BytesIO(base64.b64decode(patient.image))
        sheet.insert_image(i, 0, "image.png", {'image_data':
                           patient_image, 'x_scale': 0.1, 'y_scale': 0.1})
      sheet.write(i, 1, patient.id)
      sheet.write(i, 2, patient.reference)
      sheet.write(i, 3, patient.partner_id.name)
      if patient.responsible_id:
        sheet.write(i, 4, patient.responsible_id.partner_id.name)
      sheet.write(i, 5, patient.age)
      sheet.write(i, 6, patient.gender)
      sheet.write(i, 7, patient.note)
      sheet.write(i, 9, patient.appointments_count)
      sheet.write(i, 10, patient.children_count)
      i += 1
