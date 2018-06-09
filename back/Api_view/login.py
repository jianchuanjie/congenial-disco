from flask import render_template, redirect, flash, url_for, request
from flask import current_app, jsonify, abort
from flask_restful import Resource, reqparse
from .. import db
from ..models import User


class Login(Resource):
    '''
    This is a Login class for RESTful API
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
        user = User.query.filter_by(username=username).first()
        if user is None or not user.verify(password):
            return jsonify({
                'code': 403,
                'message': 'username or password is wrong !',
                })
        return jsonify({
            'code': 200,
            'message': 'login success',
            })
