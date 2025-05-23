# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'summary': "Manage hospital operations.",
    "description": """
This module helps in managing hospital operations, including patient records, appointments, and billing.
It provides a user-friendly interface for healthcare professionals to streamline their workflow and improve patient care.
Key Features:
- Patient Registration: Easily register new patients and maintain their medical history.
- Appointment Scheduling: Schedule and manage appointments for patients and doctors.
- Billing and Invoicing: Generate invoices for medical services and track payments.
- Reporting: Generate reports on patient visits, billing, and other key metrics.
- User Management: Manage user roles and permissions for healthcare staff.
- Customizable: Tailor the module to fit the specific needs of your hospital or clinic.
- Responsive Design: Access the module from any device, including tablets and smartphones.
- Integration: Seamlessly integrate with other Odoo modules for a complete hospital management solution.
""",
    'author': "AbdoPrDZ",
    'website': "https://github.com/AbdoPrDZ/odoo-om_hospital",
    'license': 'AGPL-3',
    'support': 'https://github.com/AbdoPrDZ/odoo-om_hospital/issues',
    'category': 'Productivity/Other',
    'version': '14.0.1.0.0',
    'sequence': 10,
    'depends': ['base', 'sale', 'mail', 'report_xlsx'],
    "data": [
        "data/ir_sequence_data.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/menu.xml",
        "wizard/create_appointment_view.xml",
        "wizard/create_appointment_report_view.xml",
        "views/patient_female.xml",
        "views/patient_kids.xml",
        "views/patient_male.xml",
        "views/patient.xml",
        "views/appointment.xml",
        "views/medicine.xml",
        "views/reception.xml",
        "views/doctor.xml",
        "views/sale.xml",
        "views/partner.xml",
        "views/templates/doctors_template.xml",
        "views/templates/doctor_template.xml",
        "views/templates/appointments_template.xml",
        "views/assets.xml",
        "report/patient_report_template.xml",
        "report/patient_report.xml",
        "report/patient_report_xlsx.xml",
        "report/appointment_report_template.xml",
        "report/appointment_report.xml",
        "report/appointment_report_xlsx.xml",
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/work_days_field.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
