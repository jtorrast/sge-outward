# -*- coding: utf-8 -*-
# from odoo import http


# class Provesubuntu(http.Controller):
#     @http.route('/provesubuntu/provesubuntu', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/provesubuntu/provesubuntu/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('provesubuntu.listing', {
#             'root': '/provesubuntu/provesubuntu',
#             'objects': http.request.env['provesubuntu.provesubuntu'].search([]),
#         })

#     @http.route('/provesubuntu/provesubuntu/objects/<model("provesubuntu.provesubuntu"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('provesubuntu.object', {
#             'object': obj
#         })
