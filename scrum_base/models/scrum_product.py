# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class ProductTag(models.Model):
    _name = 'product.tag'
    _description = 'Product Tags'

    active = fields.Boolean(default=True)
    color = fields.Integer(required=True, default=0)
    name = fields.Char(required=True)


class ScrumProduct(models.Model):
    _description = "Scrum Product"
    _name = 'scrum.product'
    _inherit = ['ir.needaction_mixin', 'mail.thread']
    _order = 'id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('state', '!=', 'done')]

    name = fields.Char('Code', translate=True, default="New")
    desc = fields.Char('Name', translate=True, size=100)
    obs = fields.Text('Notes', translate=True, default="Backlog")
    access = fields.Text('Access')
    project_id = fields.Many2one('scrum.project', string='Project')
    product_owner_id = fields.Many2one('res.partner', string='Product Owner')
    scrum_master_id = fields.Many2one('res.partner', string='Scrum Master')

    tag_ids = fields.Many2many('product.tag', string='Tags')

    # Imagenes ========================================================================================================

    image_medium = fields.Binary(
        "Medium-sized image",
        help="Product image")

    @api.one
    def _set_image_medium(self):
        self._set_image_value(self.image_medium)


    # STORY ############################################################

    story_count = fields.Integer('Story', compute="_get_story_count")
    story_ids = fields.One2many('scrum.user.story', 'product_id', 'Story')

    @api.multi
    @api.depends('story_ids')
    def _get_story_count(self):
        for product in self:
            product.story_count = len(product.story_ids)

    @api.multi
    def action_view_story(self):
        storys = self.mapped('story_ids')
        action = self.env.ref('scrum_base.action_scrum_user_story').read()[0]
        if len(storys) > 0:
            action['domain'] = [('id', 'in', storys.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    # STORY ############################################################

    task_count = fields.Integer('Task', compute="_get_task_count")
    task_ids = fields.One2many('scrum.user.task', 'product_id', 'Task')

    @api.multi
    @api.depends('task_ids')
    def _get_task_count(self):
        for product in self:
            product.task_count = len(product.story_ids)

    @api.multi
    def action_view_task(self):
        tasks = self.mapped('task_ids')
        action = self.env.ref('scrum_base.action_scrum_user_task').read()[0]
        if len(tasks) > 0:
            action['domain'] = [('id', 'in', tasks.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    # REVIEW ############################################################

    review_count = fields.Integer('Review', compute="_get_review_count")
    review_ids = fields.One2many('scrum.review', 'product_id', 'Review')

    @api.multi
    @api.depends('review_ids')
    def _get_review_count(self):
        for product in self:
            product.review_count = len(product.review_ids)

    @api.multi
    def action_view_review(self):
        reviews = self.mapped('review_ids')
        action = self.env.ref('scrum_base.action_scrum_review').read()[0]
        if len(reviews) > 0:
            action['domain'] = [('id', 'in', reviews.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    # BUG ############################################################

    bug_count = fields.Integer('Review', compute="_get_bug_count")
    bug_ids = fields.One2many('scrum.user.bug', 'product_id', 'Bugs')

    @api.multi
    @api.depends('bug_ids')
    def _get_bug_count(self):
        for product in self:
            product.bug_count = len(product.bug_ids)

    @api.multi
    def action_view_bug(self):
        bugs = self.mapped('bug_ids')
        action = self.env.ref('scrum_base.action_scrum_user_bug1').read()[0]
        if len(bugs) > 0:
            action['domain'] = [('id', 'in', bugs.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    # BOOK ############################################################

    book_count = fields.Integer('Book', compute="_get_book_count")
    book_ids = fields.One2many('scrum.book', 'product_id', 'Books')

    @api.multi
    @api.depends('book_ids')
    def _get_book_count(self):
        for product in self:
            product.book_count = len(product.book_ids)

    @api.multi
    def action_view_book(self):
        books = self.mapped('book_ids')
        action = self.env.ref('scrum_base.action_scrum_book').read()[0]
        if len(books) > 0:
            action['domain'] = [('id', 'in', books.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action

    entry_date = fields.Datetime('Date', default=fields.Datetime.now)
    end_date = fields.Datetime('End Date')

    state = fields.Selection([
        ('to_do', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done')],
        string='State', index=True, readonly=True, default='to_do', copy=False)

    @api.multi
    def exe_doing(self):
        for record in self:
            record.state = 'doing'
            record.message_post(body=_("Doing: %s") % record.env.user.name)

    @api.multi
    def exe_done(self):
        for record in self:
            record.state = 'done'
            record.message_post(body=_("Done: %s") % record.env.user.name)
            record.end_date = fields.Datetime.now()

    @api.multi
    def exe_open(self):
        for record in self:
            record.state = 'to_do'
            record.message_post(body=_("To Do: %s") % record.env.user.name)

    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('scrum.product') or "New"
        return super(ScrumProduct, self).create(vals)

    @api.multi
    def name_get(self):
        res = super(ScrumProduct, self).name_get()
        result = []
        for element in res:
            product_id = element[0]
            code = self.browse(product_id).name
            desc = self.browse(product_id).desc
            name = code and '[%s] %s' % (code, desc) or '%s' % desc
            result.append((product_id, name))
        return result