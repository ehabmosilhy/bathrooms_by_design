# -*- encoding: utf-8 -*-
from openerp import tools
from openerp import models, fields


class UserTaskReport(models.Model):
    _name = 'user.task.report'
    _description = "User Task report"
    _auto = False

    id = fields.Integer("ID")
    user_id = fields.Many2one('res.users')
    user_name = fields.Char('User Name')
    name = fields.Char(related='user_id.partner_id.name')
    image = fields.Binary(related='user_id.partner_id.image')
    project_name = fields.Char('Project')
    open_tasks = fields.Integer('Open')
    delayed = fields.Integer('Delayed')
    finished_this_month = fields.Integer('Finished this month')
    finished_last_week = fields.Integer('Finished last week')

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'user_task_report')

        cr.execute("""
                create or replace view user_task_report as (
               select 
                    u.id as user_id, u.login as user_name
                    , a."name" as project_name
                    ,(select count(id) from project_task where user_id=u.id and project_id=p.id and stage_id<7) as open_tasks
                    ,(select count(id) from project_task where user_id=u.id and project_id=p.id and stage_id<7 and date_deadline <DATE 'tomorrow' ) as delayed
                    ,(select count(id) from project_task where user_id=u.id and project_id=p.id and stage_id=7 and date_last_stage_update >= date_trunc('month', CURRENT_DATE)) as finished_this_month
                    ,(select count(id) from project_task where user_id=u.id and project_id=p.id and stage_id=7 and date_last_stage_update  BETWEEN
                        NOW()::DATE-EXTRACT(DOW FROM NOW())::INTEGER-7 
                        AND NOW()::DATE-EXTRACT(DOW from NOW())::INTEGER) as finished_last_week
                    , CONCAT(u.id, p.id) as id
                    from res_users u 
                    inner join project_task t on t.user_id=u.id
                    inner join project_project p on p.id=t.project_id
                    inner join account_analytic_account a on a.id=p.analytic_account_id
                    group by  u.id, u.login, a.name, open_tasks,finished_last_week,finished_this_month,delayed, p.id
                    order by u.login
                       )""")



