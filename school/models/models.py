# -*- coding: utf-8 -*-

from odoo import models, fields, api


class student(models.Model):
      _name = 'school.student'
      _description = 'The Students'

      name = fields.Char()
      year = fields.Integer()
      topics = fields.Many2many('school.topic')
      passed_topics = fields.Many2many(comodel_name='school.topic',
                                       relation='passed_topic_students',
                                       column1= 'student_id',
                                       column2='topic_id')
      qualifications = fields.One2many('school.qualification', 'student')

class topic(models.Model):
    _name = 'school.topic'
    _description = 'Topics'

    name = fields.Char()
    teacher = fields.Many2one('school.teacher')
    teacher_phone = fields.Char(related='teacher.phone')
    students = fields.Many2many('school.student')
    passed_students = fields.Many2many(comodel_name='school.student',
                                     relation='passed_topic_students',
                                     column1='topic_id',
                                     column2='student_id')
    qualifications = fields.One2many('school.qualification', 'topic')

class teacher(models.Model):
    _name = 'school.teacher'
    _description = 'Teachers'

    name = fields.Char()
    phone = fields.Char()
    year = fields.Integer()
    topics = fields.One2many('school.topic','teacher')

class qualification(models.Model):
    _name = 'school.qualification'
    _description = 'Student Qualification'

    student = fields.Many2one('school.student')
    topic = fields.Many2one('school.topic')
    qualification = fields.Float()
    passes = fields.Boolean(compute='_get_passes')

    @api.depends('qualification')
    def _get_passes(self):
        for q in self:
            print(q,self)
            if q.qualification >= 5:
                q.passes = True
            else:
                q.passes = False
