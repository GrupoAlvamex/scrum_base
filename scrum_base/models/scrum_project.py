# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError


class ProjectTag(models.Model):
    _name = 'project.tag'
    _description = 'Project Tags'

    active = fields.Boolean(default=True)
    color = fields.Integer(required=True, default=0)
    name = fields.Char(required=True)


class ScrumProject(models.Model):
    _description = "Scrum Project"
    _name = 'scrum.project'
    _inherit = ['ir.needaction_mixin', 'mail.thread']
    _order = 'id desc'

    @api.model
    def _needaction_domain_get(self):
        return [('state', '!=', 'done')]

    name = fields.Char('Code', translate=True, default="New")
    desc = fields.Char('Name', translate=True, size=100)
    obs = fields.Text('Notes', translate=True)
    tag_ids = fields.Many2many('project.tag', string='Tags')

    partner_id = fields.Many2one('res.partner', string='Partner')

    entry_date = fields.Datetime('Date', default=fields.Datetime.now)
    end_date = fields.Datetime('End Date')

    state = fields.Selection([
        ('to_do', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done')],
        string='State', index=True, readonly=True, default='to_do', copy=False)

    product_count = fields.Integer('Product', compute="_get_product_count")
    product_ids = fields.One2many('scrum.product', 'project_id', 'Product')


    image_medium = fields.Binary(
        "Medium-sized image",
        help="Product image")

    @api.one
    def _set_image_medium(self):
        self._set_image_value(self.image_medium)

    @api.multi
    @api.depends('product_ids')
    def _get_product_count(self):
        for project in self:
            project.product_count = len(project.product_ids)


    @api.multi
    def action_view_products(self):
        products = self.mapped('product_ids')
        action = self.env.ref('scrum_base.action_scrum_product').read()[0]
        if len(products) > 0:
            action['domain'] = [('id', 'in', products.ids)]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action


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
            vals['name'] = self.env['ir.sequence'].next_by_code('scrum.project') or "New"
        return super(ScrumProject, self).create(vals)

    @api.multi
    def name_get(self):
        res = super(ScrumProject, self).name_get()
        result = []
        for element in res:
            project_id = element[0]
            code = self.browse(project_id).name
            desc = self.browse(project_id).desc
            name = code and '[%s] %s' % (code, desc) or '%s' % desc
            result.append((project_id, name))
        return result