# -*- coding: utf-8 -*-
# from odoo import http


# class Vivero(http.Controller):
#     @http.route('/vivero/vivero/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vivero/vivero/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('vivero.listing', {
#             'root': '/vivero/vivero',
#             'objects': http.request.env['vivero.vivero'].search([]),
#         })

#     @http.route('/vivero/vivero/objects/<model("vivero.vivero"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vivero.object', {
#             'object': obj
#         })
