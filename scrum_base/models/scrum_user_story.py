# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class ScrumUserStory(models.Model):
    _description = "User Story"
    _name = 'scrum.user.story'
    _inherit = ['ir.needaction_mixin', 'mail.thread']
    _order = 'id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('state', '!=', 'done')]

    name = fields.Char('Code', translate=True, default="New")
    desc = fields.Char('Name', translate=True, size=100)
    difficulty = fields.Selection([
        ('0', '0'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('5', '5'),
        ('8', '8'),
        ('13', '13'),
        ('20', '20'),
        ('40', '40'),
        ('100', '100')],
        string='Planning Poker',default='3', copy=False)

    obs_how = fields.Text('How', translate=True , default="How")
    obs_want = fields.Text('Want', translate=True, default="Want")
    obs_for = fields.Text('For', translate=True, default="For")
    obs_terms = fields.Text('Terms', translate=True, default="Term")


    developer_id = fields.Many2one('res.partner', string='Scrum Developer')
    product_id = fields.Many2one('scrum.product', string='Product')


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
            vals['name'] = self.env['ir.sequence'].next_by_code('scrum.user.story') or "New"
        return super(ScrumUserStory, self).create(vals)

    @api.multi
    def name_get(self):
        res = super(ScrumUserStory, self).name_get()
        result = []
        for element in res:
            product_id = element[0]
            code = self.browse(product_id).name
            desc = self.browse(product_id).desc
            name = code and '[%s] %s' % (code, desc) or '%s' % desc
            result.append((product_id, name))
        return result