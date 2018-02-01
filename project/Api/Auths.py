from flask import request,make_response,g,current_app,jsonify
from flask_restful import Resource
from project.models import User
from project.extra import login_required

class auth(Resource):
    def post(self):
        #创建用户对象
        user = User(request.json.get('username'))
        
        if user.verify_password(request.json.get('password')):
            g.user = user
            return jsonify(status = 1,token = g.user.generate_auth_token())
        else:
            return jsonify(status = 0,message = "failed")

class use_auth(Resource):
    @login_required
    def post(self):
        return jsonify(status = 1, message = "success")

