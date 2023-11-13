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
     colonist = fields.Integer()

     def generate_colonist(self):
         #para comprobar edificio recorrer con un for los edificios y camviar una variable bool a true si lo encuentra

         for p in self:
             for building in p.building:
                 have_barrack = False
                 print(building.name)
                 if building.name == 'Barrack':
                     have_barrack = True
                     print("Tienes BARRACK")
                     break
             if not have_barrack:
                 raise ValidationError("You need some Barracks")

             if p.food >= 50 and have_barrack:
                 p.colonist = p.colonist + 1
                 print("Colonist +1", p.colonist)
             else:
                 raise ValidationError("You don't have enough food")





     @api.depends('building')
     def _get_resource(self):
         for player in self:
             player.gold = 0
             player.wood = 0
             player.stone = 0
             player.food = 0
             for building in player.building:
                 player.gold += building.gold_production
                 player.wood += building.wood_production
                 player.stone += building.stone_production
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
    name = fields.Char(compute='_get_name')
    food_production = fields.Integer()
    wood_production = fields.Integer()
    stone_production = fields.Integer()
    gold_production = fields.Integer()
    soldier_production = fields.Integer()
    colonist_production = fields.Integer()
    food_cost = fields.Integer()
    wood_cost = fields.Integer()
    stone_cost = fields.Integer()
    gold_cost = fields.Integer()
    construction_time = fields.Integer()
    img = fields.Image(max_width=200, max_height=200)

    @api.depends('type')
    def _get_name(self):
        for b in self:
            b.name = b.type

class player_building(models.Model):
    _name = 'outward.player_building'
    _description = 'Player Buildings'

    type = fields.Many2one('outward.building')
    player = fields.Many2one('outward.player')
    name = fields.Char(compute='_get_name')
    #campo nombre con constrais para probar que no sea repetido
    building_level = fields.Integer(default=1)
    food_production = fields.Integer(compute='_get_production')
    wood_production = fields.Integer(compute='_get_production')
    stone_production = fields.Integer(compute='_get_production')
    gold_production = fields.Integer(compute='_get_production')
    soldier_production = fields.Integer(compute='_get_production')
    colonist_production = fields.Integer(compute='_get_production')

    @api.depends('player')
    def _get_name(self):
        for b in self:
            b.name = b.type.name + " de " + b.player.name + ". ID: " + str(b.id)

    @api.depends('type')
    def _get_production(self):
        for b in self:
            b.food_production = b.type.food_production + b.type.food_production * math.log(b.building_level)
            b.wood_production = b.type.wood_production + b.type.wood_production * math.log(b.building_level)
            b.stone_production = b.type.stone_production + b.type.stone_production * math.log(b.building_level)
            b.gold_production = b.type.gold_production + b.type.gold_production * math.log(b.building_level)
            b.soldier_production = b.type.soldier_production + b.type.soldier_production * math.log(b.building_level)
            b.colonist_production = b.type.colonist_production + b.type.colonist_production * math.log(b.building_level)


#pensar sistemas de defensa

#modelo soldados y soldados_jugador:
#guard -> barrack. Coste 60 food, 20 gold, 20 seg
#cowboy-> establo, food 25, gold 45, 25 seg
#marshals-> fuerte, food 60, gold 75, 30 seg