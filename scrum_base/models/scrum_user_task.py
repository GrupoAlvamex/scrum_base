# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class ScrumUserTask(models.Model):
    _description = "User Task"
    _name = 'scrum.user.task'
    _inherit = ['ir.needaction_mixin', 'mail.thread']
    _order = 'priority , id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('state', '!=', 'delivery')]

    name = fields.Char('Code', translate=True, default="New")
    desc = fields.Char('Name', translate=True, size=100)
    count = fields.Integer('Count',default=1)
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
        string='Planning Poker', default='3', copy=False)

    priority = fields.Selection([
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
        string='Priority', default='5', copy=False)

    obs = fields.Text('How', translate=True , default="Obs")


    developer_id = fields.Many2one('res.users', string='Scrum Developer')
    assigned_id = fields.Many2one('res.users', string='Who Assigned')

    product_id = fields.Many2one('scrum.product', string='Product')
    story_id = fields.Many2one('scrum.user.story', string='User Story')


    entry_date = fields.Datetime('Create Date', default=fields.Datetime.now)
    begin_date = fields.Datetime('Begin Date')
    end_date = fields.Datetime('End Date')

    time_duration = fields.Selection([
        ('2', '2'),
        ('4', '4'),
        ('6', '6'),
        ('8', '8')],
        string='Hours', default='4')

    state = fields.Selection([
        ('to_do', 'To Do'),
        ('assigned', 'Assigned'),
        ('doing', 'Doing'),
        ('done', 'Done'),
        ('qa', 'QA'),
        ('delivery', 'Delivery')],
        string='State', index=True, readonly=True, default='to_do', copy=False)

    @api.multi
    def exe_assigned(self):
        if not self.developer_id:
            raise UserError(_('You need a Developer'))
        for record in self:
            record.state = 'assigned'
            record.sudo().assigned_id = record.env.user
            record.message_post(body=_("Assigned to : %s") % record.developer_id.name)

    @api.multi
    def exe_doing(self):
        for record in self:
            record.state = 'doing'
            record.message_post(body=_("Doing: %s") % record.env.user.name)
            record.begin_date = fields.Datetime.now()

    @api.multi
    def exe_done(self):
        for record in self:
            record.state = 'done'
            record.message_post(body=_("Done: %s") % record.env.user.name)

    @api.multi
    def exe_qa(self):
        for record in self:
            record.state = 'qa'
            record.message_post(body=_("QA: %s") % record.env.user.name)

    @api.multi
    def exe_delivery(self):
        for record in self:
            record.state = 'delivery'
            record.message_post(body=_("Delivery: %s") % record.env.user.name)
            record.end_date = fields.Datetime.now()

    @api.multi
    def exe_i_want(self):
        for record in self:
            record.sudo().state = 'assigned'
            record.sudo().developer_id = record.env.user
            record.sudo().assigned_id = record.env.user
            record.sudo().message_post(body=_("Assigned to : %s") % record.env.user.name)

    @api.multi
    def exe_open(self):
        for record in self:
            record.state = 'to_do'
            record.message_post(body=_("To Do: %s") % record.env.user.name)
            record.count = record.count + 1

    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('scrum.user.story') or "New"
        return super(ScrumUserTask, self).create(vals)

    @api.multi
    def name_get(self):
        res = super(ScrumUserTask, self).name_get()
        result = []
        for element in res:
            product_id = element[0]
            code = self.browse(product_id).name
            desc = self.browse(product_id).desc
            name = code and '[%s] %s' % (code, desc) or '%s' % desc
            result.append((product_id, name))
        return result