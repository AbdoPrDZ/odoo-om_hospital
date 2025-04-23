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

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Productivity/Other',
    'version': '14.0.1.0.0',
    'sequence': 10,

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/patient.xml',
        'views/sale.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    # assets
    'qweb': [
        'static/src/xml/hospital.xml',
    ],
    # Other assets
    'assets': {
        'web.assets_backend': [
        ],
        'web.assets_qweb': [
        ],
    },

    # Installation
    'installable': True,
    'application': True,
    'auto_install': False,
}
