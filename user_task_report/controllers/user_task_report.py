# -*- coding: utf-8 -*-
import json

from openerp import http
from openerp.http import request


class UserTaskAPI(http.Controller):
    @http.route('/api/user_task_report', type='http', auth="none", csrf=False)
    def index(self, **args):
        try:
            cr = request.cr
            super_user_id = 1

            user_name = args.get('user_name')
            domain = [('user_name', '=', user_name)] if user_name else []

            fields = ['name', 'project_name', 'open_tasks', 'delayed', 'finished_this_month', 'finished_last_week']

            report = request.registry['user.task.report'].search_read(cr, super_user_id, domain, fields=fields)
            _response = {"data": report, "itemsCount": 0, "success": True, "statusCode": 200,
                         "message": "Data Fetched Successfully"}
            return json.dumps(_response)
        except Exception as e:
            _response = {"data": None, "itemsCount": 0, "success": False, "statusCode": 500, "message": str(e)}
            return json.dumps(_response)
