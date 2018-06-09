from flask import render_template, redirect, flash, url_for, request
from flask import current_app, jsonify, abort
from flask_restful import Resource, reqparse
from .. import db
from ..models import User


class Register(Resource):
    '''
    This is a Register class for RESTful API
    @param: username
    @param: password
    '''

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)


    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        password = args['password']

        if username is None or password is None:
            abort(400)
        user = User(username=username, password=password)
        print(user)
        try:
            db.session.add(user)
            db.session.commit()
            print("Register user successfully")
            return jsonify({
                'code': 200,
                })
        except:
            print("Register user failed")
            return jsonify({
                'code': 400,
                })
