# -*- coding: utf-8 -*-
import json

from openerp import http
from openerp.http import request


def get_user_data(user_id):
    user_data = {
        'name': user_id.name
        , 'phone': user_id.phone or ''
        , 'email': user_id.email or ''
    }
    return user_data


class Login(http.Controller):

    @http.route('/api/login', type='http', auth="none", csrf=False)
    def index(self, **args):

        db = request.env.cr.dbname

        login = args.get('login')
        password = args.get('password')

        _response = {"data": None, "itemsCount": 0, "success": False, "statusCode": 404,
                     "message": ""}
        if not login:
            _response["message"] = "Missing Login"
            return json.dumps(_response)

        if not password:
            _response["message"] = "Missing Password"
            return json.dumps(_response)

        user = request.env['res.users'].sudo().search([('login', '=', login)])
        if not user:
            _response["message"] = "Login or Password incorrect!"
            return json.dumps(_response)

        try:
            success = request.session.authenticate(db, login, password)
            if success:
                user_data = get_user_data(user)
                _response = {"data": user_data, "itemsCount": 0, "success": True, "statusCode": 200,
                             "message": "Login Successful"}
                return json.dumps(_response)
            else:
                _response = {"data": None, "itemsCount": 0, "success": False, "statusCode": 404,
                             "message": "Login or Password Incorrect !"}
                return json.dumps(_response)
        except Exception as e:
            _response = {"data": None, "itemsCount": 0, "success": False, "statusCode": 500, "message": str(e)}
            return json.dumps(_response)
