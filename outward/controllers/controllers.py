# -*- coding: utf-8 -*-
# from odoo import http


# class Outward(http.Controller):
#     @http.route('/outward/outward', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/outward/outward/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('outward.listing', {
#             'root': '/outward/outward',
#             'objects': http.request.env['outward.outward'].search([]),
#         })

#     @http.route('/outward/outward/objects/<model("outward.outward"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('outward.object', {
#             'object': obj
#         })
