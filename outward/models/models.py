# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError
import math
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# ctrl + alt + L -> dar formato al código

class player(models.Model):
    _name = 'outward.player'
    _description = 'Player'

    name = fields.Char()
    building = fields.One2many('outward.player_building', 'player')  # model players_building
    level = fields.Integer()
    gold = fields.Integer()  # computed recorriendo el building para obtener la produccion de gold
    wood = fields.Integer()
    food = fields.Integer()
    stone = fields.Integer()
    colonist = fields.Integer()
    attack = fields.Integer(compute='_get_militia_stats', store=True)
    defence = fields.Integer(compute='_get_militia_stats', store=True)
    available_buildings = fields.Many2many('outward.building', compute='_get_available_buildings')
    militia = fields.One2many('outward.player_militia', 'player')
    available_militia = fields.Many2many('outward.militia_type', compute='_get_available_militia')
    battles = fields.Many2many('outward.battle')

    @api.depends('militia.attack', 'militia.defence', 'militia.level')
    def _get_militia_stats(self):
        for player in self:
            active_militia = player.militia.filtered(lambda m: m.level > 0)
            player.attack = sum(active_militia.mapped('attack'))
            player.defence = sum(active_militia.mapped('defence'))

    def _get_available_buildings(self):
        for c in self:
            print(c)
            c.available_buildings = self.env['outward.building'].search([]).filtered(lambda b: b.wood_cost <= c.wood and
                                                                                               b.stone_cost <= c.stone).ids

    def _get_available_militia(self):
        for b in self:
            b.available_militia = self.env['outward.militia_type'].search([]).filtered(lambda c: c.gold_cost <= b.gold).ids



    def generate_colonist(self):
        # para comprobar edificio recorrer con un for los edificios y camviar una variable bool a true si lo encuentra

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

    def update_resources(self):
        for player in self.search([]):
            gold = player.gold
            wood = player.wood
            stone = player.stone
            food = player.food
            for building in player.building:
                gold += building.gold_production
                wood += building.wood_production
                stone += building.stone_production
                food += building.food_production
            player.gold = gold
            player.wood = wood
            player.stone = stone
            player.food = food


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
    # comprobar si el selection se muestra en la vista
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

    def build_building(self):
        for b in self:
            player_id = self._context.get('player_id')
            building = self.env['outward.player_building'].create({
                "type": b.id,
                "player": player_id
            })
            building_type = b.type
            if building_type.stone_cost > 0:
                building.player.stone -= building.stone_cost
                pass
            building.player.wood -= building.wood_cost


class player_building(models.Model):
    _name = 'outward.player_building'
    _description = 'Player Buildings'

    type = fields.Many2one('outward.building')
    player = fields.Many2one('outward.player')
    name = fields.Char(compute='_get_name')
    estate = fields.Selection([('Construcción', 'Construcción'), ('Operativo', 'Operativo'), ('Mejora', 'Mejora')],
                              required=True, default='Construcción')
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
            b.name = str(b.type.name) + " de " + str(b.player.name) + ". ID: " + str(b.id)

    @api.depends('type')
    def _get_production(self):
        for b in self:
            b.food_production = b.type.food_production + b.type.food_production * math.log(b.building_level + 1)
            b.wood_production = b.type.wood_production + b.type.wood_production * math.log(b.building_level + 1)
            b.stone_production = b.type.stone_production + b.type.stone_production * math.log(b.building_level + 1)
            b.gold_production = b.type.gold_production + b.type.gold_production * math.log(b.building_level + 1)
            b.soldier_production = b.type.soldier_production + b.type.soldier_production * math.log(
                b.building_level + 1)
            b.colonist_production = b.type.colonist_production + b.type.colonist_production * math.log(
                b.building_level + 1)

    # def cron_building_construcion(self):
    #   for b in self([]):
    # el cron se actualiza cada minuto pero tenemos que ir acumuldo los minutos en una variable para que los
    # los sume cada minuto y cuando esa variable sea = construction:time cambia de estado operativo y ya puede producir
    # Si cambiamos a estado mejora sube de nivel si tenemos los recursos necesarios para la subida


class militia_type(models.Model):
    _name = 'outward.militia_type'
    _description = 'Militia'

    name = fields.Char()
    attack = fields.Float()
    defence = fields.Float()
    gold_cost = fields.Float()

    def hire(self):
        for b in self:
            player_id = self._context.get('player_id')
            militia = self.env['outward.player_militia'].create({
                "type": b.id,
                "player": player_id
            })
            militia.player.gold -= militia.gold_cost


class player_militia(models.Model):
    _name = 'outward.player_militia'
    _description = 'Players Militia'

    name = fields.Char(compute='get_name_militia')
    type = fields.Many2one('outward.militia_type')
    player = fields.Many2one('outward.player')
    level = fields.Integer(default=0)
    hire_percent = fields.Float(default=0)
    attack = fields.Float(compute='_get_stats')
    defence = fields.Float(compute='_get_stats')
    gold_cost = fields.Float(compute='_get_stats')
    is_active = fields.Boolean(compute='_get_is_active')

    @api.depends('player')
    def _get_is_active(self):
        for b in self:
            b.is_active = True
            if b.attack < 0 and b.player.attack <= abs(b.attack):
                b.is_active = False
            if b.defence < 0 and b.player.defence <= abs(b.defence):
                b.is_active = False
    @api.depends('type', 'player')
    def get_name_militia(self):
        for b in self:
            b.name = 'undefined'
            if b.type and b.player:
                b.name = b.type.name + " " + b.player.name + " " + str(b.id)

    @api.depends('type')
    def _get_stats(self):
        for b in self:
            b.attack = b.type.attack + b.type.attack * math.log(b.level + 1)
            b.defence = b.type.defence + b.type.defence * math.log(b.level + 1)
            b.gold_cost = b.type.gold_cost * b.level

    def hire_level(self):
        for b in self.search([('hire_percent','<',100)]):
            b.hire_percent += 1/(b.level+1)
            if(b.hire_percent >= 100):
                b.hire_percent = 100
                b.level += 1
            print(b.name,b.hire_percent)


class battle(models.Model):
    _name = 'outward.battle'
    _description = 'Battles'

    name = fields.Char()
    start = fields.Datetime(default = lambda self: fields.Datetime.now())
    end = fields.Datetime(compute = '_get_data_end')
    total_time = fields.Integer(compute = '_get_date_end')
    remaining_time = fields.Char(compute = '_get_date_end')
    progress = fields.Float(compute='_get_date_end')
    player1 = fields.Many2one('outward.player', domain="[('id','!=',player2)]")
    player2 = fields.Many2one('outward.player', domain="[('id','!=',player1)]")


    @api.constrains('city1','city2')
    def _check_cities(self):
        for b in self:
            if b.city1.id == b.city2.id:
                raise ValidationError("One city can attack itself")



# pensar sistemas de defensa

# modelo soldados y soldados_jugador:
# guard -> barrack. Coste 60 food, 20 gold, 20 seg
# cowboy-> establo, food 25, gold 45, 25 seg
# marshals-> fuerte, food 60, gold 75, 30 seg
