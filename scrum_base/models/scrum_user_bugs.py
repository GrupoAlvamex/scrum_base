# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

class ScrumUserBugs(models.Model):
    _description = "Developer Bugs"
    _name = 'scrum.user.bug'
    _inherit = ['ir.needaction_mixin', 'mail.thread']
    _order = 'id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('state', '!=', 'delivery')]

    name = fields.Char('Code', translate=True, default="New")
    desc = fields.Char('Name', translate=True, size=100)
    difficulty = fields.Integer('Difficulty', size=100)



    obs = fields.Text('How', translate=True , default="Obs")


    developer_id = fields.Many2one('res.users', string='Scrum Developer')
    product_id = fields.Many2one('scrum.product', string='Product')
    task_id = fields.Many2one('scrum.user.task', string='Task')



    entry_date = fields.Datetime('Date', default=fields.Datetime.now)
    end_date = fields.Datetime('End Date')

    state = fields.Selection([
        ('to_do', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done'),
        ('qa', 'QA'),
        ('delivery', 'Delivery')],
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
            # record.end_date = fields.Datetime.now()

    @api.multi
    def exe_qa(self):
        for record in self:
            record.state = 'qa'
            record.message_post(body=_("QA: %s") % record.env.user.name)
            # record.end_date = fields.Datetime.now()

    @api.multi
    def exe_delivery(self):
        for record in self:
            record.state = 'delivery'
            record.message_post(body=_("Delivery: %s") % record.env.user.name)
            record.end_date = fields.Datetime.now()

    @api.multi
    def exe_open(self):
        for record in self:
            record.state = 'to_do'
            record.message_post(body=_("To Do: %s") % record.env.user.name)

    @api.model
    def create(self, vals):
        if vals.get('name', "New") == "New":
            vals['name'] = self.env['ir.sequence'].next_by_code('scrum.user.bug') or "New"
        return super(ScrumUserBugs, self).create(vals)

    file_name = fields.Char("File")
    file_01 = fields.Binary(
        string='File',
        copy=False,
        help='File')

    @api.multi
    def name_get(self):
        res = super(ScrumUserBugs, self).name_get()
        result = []
        for element in res:
            product_id = element[0]
            code = self.browse(product_id).name
            desc = self.browse(product_id).desc
            name = code and '[%s] %s' % (code, desc) or '%s' % desc
            result.append((product_id, name))
        return result