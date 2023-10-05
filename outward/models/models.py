# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
     _name = 'outward.player'
     _description = 'Player'

     name = fields.Char()
     level = fields.Integer()

class skill(models.Model):
    _name = 'outward.skill'
    _description = 'Skills'

    name = fields.Char()
    description = fields.Char()

class player_skill_level(models.Model):
    _name = 'outward.player_skill_level'
    _description = 'Player Skills'

    player_id = fields.Many2one('outward.player')
    skill_id = fields.Many2one('outward.skill')
    skill_level = fields.Integer()

class building(models.Model):
    _name = 'outward.building'
    _description = 'Buildings'