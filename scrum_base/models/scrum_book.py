# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class BookTag(models.Model):
    _name = 'book.tag'
    _description = 'Book Tags'

    active = fields.Boolean(default=True)
    color = fields.Integer(required=True, default=0)
    name = fields.Char(required=True)

class ScrumBook(models.Model):
    _description = "Scrum Book"
    _name = 'scrum.book'
    _inherit = ['ir.needaction_mixin', 'mail.thread']
    _order = 'id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('name', '!=', '')]

    name = fields.Char('Code', translate=True, default="New")
    desc = fields.Char('Name', translate=True, size=100)
    obs = fields.Text('Notes', translate=True)
    date = fields.Datetime('Date', default=fields.Datetime.now)
    product_id = fields.Many2one('scrum.product', string='Product')

    tag_ids = fields.Many2many('book.tag', string='Tags')

    image_medium = fields.Binary(
        "Medium-sized image",
        help="Product image")

    file_name = fields.Char("File")
    file_01 = fields.Binary(
        string='File',
        copy=False,
        help='File')



    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('scrum.book') or "New"
        return super(ScrumBook, self).create(vals)

    @api.multi
    def name_get(self):
        res = super(ScrumBook, self).name_get()
        result = []
        for element in res:
            book_id = element[0]
            code = self.browse(book_id).name
            desc = self.browse(book_id).desc
            name = code and '[%s] %s' % (code, desc) or '%s' % desc
            result.append((book_id, name))
        return result