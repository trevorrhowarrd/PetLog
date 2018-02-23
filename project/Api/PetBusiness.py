import uuid
import os
from hashlib import md5
from flask_restful import Resource
from flask import jsonify, g, request, current_app
from project.extra import login_required,allowed_image
from werkzeug import secure_filename

class create_pet(Resource):
    @login_required
    def post(self):
        if g.user.create_pet(request.json):
            return jsonify(status = 1, message = "success", pet_id = "")
        else :
            return jsonify(status = 0, message = "failed")

class get_user_all_pet(Resource):
    @login_required
    def get(self):
        pet_list = g.user.get_all_pet()
        if pet_list:
            return jsonify(pet_list)
        else:
            return jsonify(status = 0, message = "failed")

class new_pet_avatar(Resource):
    @login_required
    def post(self):
        file = request.files['image']
        if file and allowed_image(file.filename):
            str1 = str(uuid.uuid1()).split("-")[0]
            str2 = secure_filename(file.filename).rsplit('.')[0]
            str3 = '.' + file.filename.rsplit('.')[1]

            m = md5()
            m.update((str1 + str2).encode ('utf-8'))

            filename = m.hexdigest()[-8:8] + str3

            file.save (os.path.join(
                current_app.config['PET_AVATAR_FOLDER'],
                filename))
            
            #文件上传成功，返回文件名
            return jsonify(status = 1,\
                    filename = filename)
        else:
            return jsonify(status = 0,\
                        message = "failed")

class get_pet_detail(Resource):
    def get(self):
        pass                