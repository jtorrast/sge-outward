# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class usuarios(models.Model):
     _name = 'res.partner'
     _inherit = 'res.partner'

     nivel_karma= fields.Integer()
     premium = fields.Boolean()
     fecha_nacimiento = fields.Datetime()
     fecha_registro = fields.Datetime(default = lambda self: fields.Datetime.now())

