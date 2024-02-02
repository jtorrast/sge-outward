# -*- coding: utf-8 -*-
# from odoo import http


# class Wanderer(http.Controller):
#     @http.route('/wanderer/wanderer', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wanderer/wanderer/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('wanderer.listing', {
#             'root': '/wanderer/wanderer',
#             'objects': http.request.env['wanderer.wanderer'].search([]),
#         })

#     @http.route('/wanderer/wanderer/objects/<model("wanderer.wanderer"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wanderer.object', {
#             'object': obj
#         })
