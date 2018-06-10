from flask import render_template, redirect, flash, url_for, request
from flask import current_app, jsonify, abort
from flask_restful import Resource, reqparse
from .utils import get_file_base64
from .. import db
from ..models import User, Photo_Path as Path


class Retrive(Resource):
    '''
    '''

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('username', type=str)


    def post(self):
        args = self.parser.parse_args()
        username = args['username']
        if username is None:
            abort(400)

        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({
                'code': 403,
                'message': 'No this user',
                })
        try:
            photo_path = Path.query.filter_by(userid=user.id).order_by(Path.id.desc()).first().path
            gpic_b64 = get_file_base64(photo_path).decode()
            return jsonify({
                'code': 200,
                'pic_b64': gpic_b64,
                })
        except:
            return jsonify({
                'code': 403,
                'message': 'Something wrong',
                })
