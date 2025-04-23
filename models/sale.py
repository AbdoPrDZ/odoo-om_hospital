# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Sale(models.Model):
  _inherit = 'sale.order'

  sale_description = fields.Text(string='Sale Description')
