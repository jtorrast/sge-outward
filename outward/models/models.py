# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
     _name = 'outward.player'
     _description = 'Player'

     name = fields.Char()
     building = fields.Many2one('')#model players_building
     level = fields.Integer()
     gold = fields.Integer() #computed recorriendo el building para obtener la produccion de gold
     wood = fields.Integer()
     stone = fields.Integer()


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

    type = fields.Char()
    gold_production = fields.Integer()

class player_building(models.Model):
    _name = 'outward.player_building'
    _description = 'Player Buildings'

    type = fields.Many2one('outward.building')
    player = fields.Many2one('outward.player')
    quantity = fields.Integer()

