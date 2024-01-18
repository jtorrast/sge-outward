# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError
import math
from datetime import datetime, timedelta

# ctrl + alt + L -> dar formato al código

class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    #_description = 'Player'

    #name = fields.Char()
    is_player = fields.Boolean(default=False)
    building = fields.One2many('outward.player_building', 'player')  # model players_building
    level = fields.Integer()
    gold = fields.Integer()
    wood = fields.Integer()
    food = fields.Integer()
    stone = fields.Integer()
    colonist = fields.Integer()
    attack = fields.Integer(compute='_get_militia_stats', store=True)
    defense = fields.Integer(compute='_get_militia_stats', store=True)
    available_buildings = fields.Many2many('outward.building', compute='_get_available_buildings')
    militia = fields.One2many('outward.player_militia', 'player')
    available_militia = fields.Many2many('outward.militia_type', compute='_get_available_militia')
    battles = fields.Many2many('outward.battle')

    @api.depends('militia.attack', 'militia.defense', 'militia.level')
    def _get_militia_stats(self):
        for player in self:
            active_militia = player.militia.filtered(lambda m: m.level > 0)
            player.attack = sum(active_militia.mapped('attack'))
            player.defense = sum(active_militia.mapped('defense'))

    def _get_available_buildings(self):
        for c in self:
            print(c)
            c.available_buildings = self.env['outward.building'].search([]).filtered(lambda b: b.wood_cost <= c.wood and
                                                                                               b.stone_cost <= c.stone).ids

    def _get_available_militia(self):
        for b in self:
            b.available_militia = self.env['outward.militia_type'].search([]).filtered(lambda c: c.gold_cost <= b.gold).ids

    def generate_colonist(self):
        for p in self:
            if p.food >= 50:
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

    player_id = fields.Many2one('res.partner')
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
    player = fields.Many2one('res.partner')
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
    defense = fields.Float()
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
    player = fields.Many2one('res.partner')
    level = fields.Integer(default=0)
    hire_percent = fields.Float(default=0)
    attack = fields.Float(compute='_get_stats')
    defense = fields.Float(compute='_get_stats')
    gold_cost = fields.Float(compute='_get_stats')
    is_active = fields.Boolean(compute='_get_is_active')

    @api.depends('player')
    def _get_is_active(self):
        for b in self:
            b.is_active = True
            if b.attack < 0 and b.player.attack <= abs(b.attack):
                b.is_active = False
            if b.defense < 0 and b.player.defense <= abs(b.defense):
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
            b.defense = b.type.defense + b.type.defense * math.log(b.level + 1)
            b.gold_cost = b.type.gold_cost * b.level

    def hire_level(self):
        for b in self.search([('hire_percent','<',100)]):
            b.hire_percent += 1/(b.level+1)
            if(b.hire_percent >= 100):
                b.hire_percent = 100
                b.level += 1
            print(b.name,b.hire_percent)

class player_militia_wizard(models.TransientModel):
    _name = 'outward.player_militia_wizard'

    name = fields.Char()
    type = fields.Many2one('outward.militia_type', required=True)
    player = fields.Many2one('outward.player', required=True)

    @api.depends('type','player')
    def _get_name(self):
        for b in self:
            b.name = 'undefined'
            if b.type and b.player:
                b.name = b.type.name + " " + b.player.name + " " + str(b.id)


    def hire_militia(self):
        self.env['outward.player_militia'].create({
            "type": self.type.id,
            "city": self.city.id
        })

class battle(models.Model):
    _name = 'outward.battle'
    _description = 'Battles'

    name = fields.Char()
    start = fields.Datetime(default = lambda self: fields.Datetime.now())
    end = fields.Datetime(compute='_get_date_end')
    remaining_time = fields.Char(compute = '_get_date_end')
    progress = fields.Float(compute='_get_date_end')
    player1 = fields.Many2one('res.partner', domain="[('id','!=',player2)]")
    player2 = fields.Many2one('res.partner', domain="[('id','!=',player1)]")
    winner = fields.Many2one('res.partner',string="Winner", readonly=True)
    finished = fields.Boolean(default=False, readonly=True)


    @api.constrains('player1','player2')
    def _check_cities(self):
        for b in self:
            if b.player1.id == b.player2.id:
                raise ValidationError("One city can attack itself")

    @api.depends('start')
    def _get_date_end(self):
        for b in self:
            date_start = fields.Datetime.from_string(b.start)
            date_end = date_start + timedelta(hours=2)
            remaining = date_end - datetime.now()
            time_past = (datetime.now() - date_start).total_seconds()/60
            b.end = fields.Datetime.to_string(date_end)
            b.remaining_time = "{:02}:{:02}:{:02}".format(remaining.seconds // 3600, (remaining.seconds // 60) % 60,
                                                          remaining.seconds % 60)
            b.progress = (time_past * 100) / (2*60)

    def calculate_battle(self, player1, player2):
        winner = None
        loser = None

        if player1.attack > player2.defense:
            winner = player1
            loser = player2
        elif player2.attack > player1.defense:
            winner = player2
            loser = player1

        if winner and loser:
            winner_gold_increase = winner.gold * 0.2
            loser_gold_decrease = loser.gold * 0.1

            winner.write({'gold': winner.gold + winner_gold_increase})
            loser.write({'gold': loser.gold - loser_gold_decrease})

            self.winner = winner


    def fight_time(self):
        for b in self.search([]):
            if not b.finished and b.progress >= 100:
                b.calculate_battle(b.player1, b.player2)
                b.finished = True


    def finish_battle(self):
        for b in self:
            if not b.finished:
                b.calculate_battle(b.player1, b.player2)
                b.progress = 100.00
                b.finished = True

class battle_wizard(models.TransientModel):
    _name = 'outward.battle_wizard'

    state = fields.Selection([
        ('player', "Players"),
        ('militia', "Milita"),
        ('dates', "Dates"),
    ], default='player')

    name = fields.Char()
    start = fields.Datetime()

    def action_next(self):
        if(self.state == 'player'):
            self.state = 'militia'
        elif(self.state == 'militia'):
            self.state = 'dates'
        return {
            'type': 'ir.actions.act_window',
            'name': 'Launch battle wizard',
            'res_model': self._name,
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
            'context': self._context
        }

    def action_previous(self):
        if(self.state == 'militia'):
            self.state = 'player'
        elif(self.state == 'dates'):
            self.state = 'militia'
        return{
            'type': 'ir.actions.act_window',
            'name': 'Launch battle wizard',
            'res_model': self._name,
            'view_mode': 'form',
            'target': 'new',
            'res_id': self.id,
            'context': self._context
        }

    def create_battle(self):
        print(self)

