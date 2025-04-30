# -*- coding: utf-8 -*-

from odoo import http


class Doctor(http.Controller):

  @http.route('/om_hospital/doctor/', website=True, auth='user')
  def index(self, **kw):
    return http.request.render('om_hospital.template_doctors', {
        'doctors': http.request.env['om_hospital.doctor'].search([]),
    })

  @http.route('/om_hospital/doctor/<model("om_hospital.doctor"):doctor>/', website=True, auth='user')
  def find(self, doctor, **kw):
    if not doctor:
      return http.request.not_found()

    return http.request.render('om_hospital.template_doctor', {
        'doctor': doctor,
        'appointments': http.request.env['om_hospital.appointment'].search(
            [('doctor_id', '=', doctor.id)])
    })

  @http.route('/om_hospital/doctor/<model("om_hospital.doctor"):doctor>/appointments', website=True, auth='user')
  def appointments(self, doctor, **kw):
    return http.request.render('om_hospital.template_appointments', {
        'appointments': http.request.env['om_hospital.appointment'].search([('doctor_id', '=', doctor.id)]),
        'doctor': doctor
    })
