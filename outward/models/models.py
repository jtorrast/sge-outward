# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class player(models.Model):
     _name = 'outward.player'
     _description = 'Player'

     name = fields.Char()
     building = fields.One2many('outward.player_building', 'player')#model players_building
     level = fields.Integer()
     gold = fields.Integer(compute='_get_resource') #computed recorriendo el building para obtener la produccion de gold
     wood = fields.Integer(compute='_get_resource')
     food = fields.Integer(compute='_get_resource')
     stone = fields.Integer(compute='_get_resource')
     colonist = fields.Integer(compute='_get_resource')

     @api.depends('building')
     def _get_resource(self):
         for player in self:
             for building in self.building:
                 player.gold += building.gold_production
                 player.wood += building.wood_production
                 player.stone += building.stone_production
                 player.colonist += building.colonist_production
                 player.food += building.food_production


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
    food_production = fields.Integer()
    wood_production = fields.Integer()
    stone_production = fields.Integer()
    gold_production = fields.Integer()
    soldier_production = fields.Integer()#ver de hacer seccion modelos para militares y desblquean según edificios
    colonist_production = fields.Integer()
    food_cost = fields.Integer()
    wood_cost = fields.Integer()
    stone_cost = fields.Integer()
    gold_cost = fields.Integer()





class player_building(models.Model):
    _name = 'outward.player_building'
    _description = 'Player Buildings'

    type = fields.Many2one('outward.building')
    player = fields.Many2one('outward.player')
    #campo nombre con constrais para probar que no sea repetido
    building_level = fields.Integer(default=1)
    food_production = fields.Integer(compute='_get_production')
    wood_production = fields.Integer(compute='_get_production')
    stone_production = fields.Integer(compute='_get_production')
    gold_production = fields.Integer(compute='_get_production')
    soldier_production = fields.Integer(compute='_get_production')
    colonist_production = fields.Integer(compute='_get_production')

    @api.depends('type')
    def _get_production(self):
        for b in self:
            b.food_production = b.type.food_production + b.type.food_production * math.log(b.building_level)
            b.wood_production = b.type.wood_production + b.type.wood_production * math.log(b.building_level)
            b.stone_production = b.type.stone_production + b.type.stone_production * math.log(b.building_level)
            b.gold_production = b.type.gold_production + b.type.gold_production * math.log(b.building_level)
            b.soldier_production = b.type.soldier_production + b.type.soldier_production * math.log(b.building_level)
            b.colonist_production = b.type.colonist_production + b.type.colonist_production * math.log(b.building_level)

