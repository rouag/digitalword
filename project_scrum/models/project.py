# -*- coding: utf-8 -*-
# © 2016 Pierre Faniel
# © 2016 Niboo SPRL (<https://www.niboo.be/>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, exceptions, fields, models


class ProjectScrumTeam(models.Model):
    _name = 'project.scrum.team'

    name = fields.Char('Name', required=True)
    sprint_ids = fields.One2many('project.sprint', 'scrum_team_id', 'Sprints')
    project_ids = fields.One2many('project.project', 'scrum_team_id',
                                  'Projects')


class ProjectProject(models.Model):
    _inherit = 'project.project'

    scrum_team_id = fields.Many2one('project.scrum.team', 'Scrum Team')


class ProjectSprint(models.Model):
    _name = 'project.sprint'
    _rec_name = 'display_name'
    name = fields.Char('Name', required=True)
    display_name = fields.Char('Display Name', compute="_compute_display_name",
                               store=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    scrum_team_id = fields.Many2one('project.scrum.team', 'Scrum Team',
                                    required=True)
    task_count = fields.Integer('# Tasks', compute='_task_count')

    is_current_sprint = fields.Boolean('Is Current Sprint')
    is_previous_sprint = fields.Boolean('Is Previous Sprint')

    @api.one
    def _task_count(self):
        tasks = self.env['project.task'].search([('sprint_id', '=', self.id)])
        self.task_count = len(tasks)

    @api.constrains("is_current_sprint")
    def check_current_sprint(self):
        self.ensure_one()
        self.check_is_not_both_previous_and_current()
        if self.is_current_sprint:
            old_previous = self.search([('is_previous_sprint', '=', True)])
            if old_previous:
                old_previous.is_previous_sprint = False
            old_current = self.search([('is_current_sprint', '=', True),
                         ('id', '!=', self.id)])
            if old_current:
                old_current.is_current_sprint = False

                old_current.is_previous_sprint = True

    @api.constrains("is_previous_sprint")
    def check_previous_sprint(self):
        self.ensure_one()
        self.check_is_not_both_previous_and_current()
        if len(self.search([('is_previous_sprint', '=', True)])) > 1:
            raise exceptions.ValidationError('A single previous sprint is '
                                             'permitted')

    @api.multi
    def check_is_not_both_previous_and_current(self):
        self.ensure_one()
        if self.is_current_sprint and self.is_previous_sprint:
            raise exceptions.ValidationError('A sprint cannot be previous'
                                             ' and current at the same time')

    @api.constrains('start_date', 'end_date')
    @api.multi
    def check_dates(self):
        for sprint in self:
            concurrent_sprints = self.search([
                '&',
                    '|',
                        '|',
                            '&',
                                ('start_date', '<=', sprint.end_date),
                                ('start_date', '>=', sprint.start_date),
                            '&',
                                ('end_date', '<=', sprint.end_date),
                                ('end_date', '>=', sprint.start_date),
                        '&',
                            ('start_date', '<=', sprint.start_date),
                            ('end_date', '>=', sprint.end_date),
                    '&',
                        ('id', '!=', sprint.id),
                        ('scrum_team_id', '=', sprint.scrum_team_id.id)
            ])
            if concurrent_sprints:
                raise exceptions.ValidationError('Sprints cannot overlap')

    @api.multi
    def view_tasks_action(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.task',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
            'name': self.name,
            'display_name': self.display_name,
            'domain': [('sprint_id', '=', self.id)],
            'context': {'default_sprint_id': self.id,}
        }

    @api.depends('name', 'start_date', 'end_date')
    def _compute_display_name(self):
        for sprint in self:
            sprint.display_name = '%s - %s/%s' % (sprint.name,
                                                  sprint.end_date[8:10],
                                                  sprint.end_date[5:7])

    _order = "start_date DESC"


class ProjectTask(models.Model):
    _inherit = 'project.task'

    sprint_id = fields.Many2one('project.sprint', 'Sprint', required=True,
                                track_visibility='onchange')

    @api.multi
    def go_to_sprint_action(self):
        self.ensure_one()
        return self.sprint_id.view_tasks_action()

    @api.multi
    def assign_to_me(self):
        self.ensure_one()
        self.user_id = self._uid
