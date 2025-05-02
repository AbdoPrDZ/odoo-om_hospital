# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Product(models.Model):
  _inherit = 'product.template'

  type = fields.Selection(selection_add=[
      ('medicine', 'Medicine'), ('service',)
  ], tracking=True, ondelete={
      'medicine': 'set default',
      # 'test': 'set null',
      # 'test': 'cascade',
  })
