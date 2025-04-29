# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Product(models.Model):
  _inherit = 'product.template'

  type = fields.Selection(selection_add=[
      ('test', 'Test'), ('service',)
  ], tracking=True, ondelete={
      'test': 'set default',
      # 'test': 'set null',
      # 'test': 'cascade',
  })
