import random
from . import mail
from flask import request, abort, current_app, g, jsonify, render_template
from functools import wraps
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from .Models.User import User
from flask_mail import Message
from threading import Thread


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False  # valid token, but expired
    except BadSignature:
        return False  # invalid token
    g.user = User.query.get(data['id'])
    return True


def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in \
           current_app.config['IMAGE_ALLOWED_EXTENSIONS']


def checke_interface(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print("Error : " + str(error.__class__) + "    " + error.__str__())
            return jsonify(status = 0,\
                        message = "failed")

    return inner


@checke_interface
def login_required(func):
    @wraps(func)
    def inner(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify(status=0, message="请重新登录")
        else:
            if verify_auth_token(token):
                return func(*args, **kwargs)
            else:
                return jsonify(status=0, message="请重新登录")

    return inner


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_registered_email(to_mail, code):
    from manage import app
    msg = Message("验证用于 PetLog 的注册", recipients=[to_mail])

    msg.html = render_template("mail.html", code=code)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
