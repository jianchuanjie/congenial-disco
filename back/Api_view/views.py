from flask import render_template, redirect, flash, url_for, request
from flask import current_app, jsonify, abort
import os, time, hashlib, base64, imghdr, json
from flask_restful import Resource, reqparse
from WC.comeonpy3 import WC_app_create, readDocument, segment,\
    FONTS_PATH, removeStopWords, wordCount, changeFre
from .utils import types, colormaps, background_colors, fonts
from .utils import from_doc_get_word_list, from_font_get_font_path,\
    from_photo_get_photo_path, get_file_base64, get_name,\
    remove_files, remove_files
from ..models import User, Photo_Path
from .. import db


class Upload(Resource):
    '''
    This is a upload class for RESTful API.
    And this is the main class for handle with
    the data that comes from XuanYun APP
    '''
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('type', type=int, default=1, choices=types)
        self.parser.add_argument('photo', type=str, required=True)
        self.parser.add_argument('doc', type=str)
        self.parser.add_argument('txt', type=str)
        self.parser.add_argument('url', type=str)
        self.parser.add_argument('max_words', type=int, default=2000)
        self.parser.add_argument('background_color', default='white',
            choices=background_colors)
        self.parser.add_argument('max_font_size', type=int, default=100)
        self.parser.add_argument('colormap', default="spring", 
            choices=colormaps)
        self.parser.add_argument('font', type=str, default='fan', choices=fonts)
        self.parser.add_argument('username', type=str)
        self.parser.add_argument('changelist', type=str)


    def get(self):
        return jsonify({'test':'test'})


    def post(self):
        args = self.parser.parse_args()
        path = {}
        try:
            path['photo'] = from_photo_get_photo_path(args['photo'])
        except:
            abort(400)

        if args['type'] == 1:
            try:
                path['doc'], word_list = from_doc_get_word_list(args['doc'])
            except:
                abort(400)
        elif args['type'] == 2:
            try:
                word_list = segment(args['txt'])
            except:
                abort(400)
        else:
            try:
                pass
            except:
                abort(404)

        if args['changelist'] is None:
            word_list = wordCount(word_list)
        else:
            changelist = args['changelist']
            changelist = json.loads(changelist.replace("'", '"'))
            word_list = changeFre(wordCount(word_list), changelist)

        path['gen'] = WC_app_create(
            seg_list=word_list,
            mask_path=path['photo'],
            max_words=args['max_words'],
            background_color=args['background_color'],
            max_font_size=args['max_font_size'],
            colormap=args['colormap'],
            font_path=from_font_get_font_path(args['font'])
            )
        gpic_b64 = get_file_base64(path['gen']).decode()

        # remove_files(path)
        if args['username'] is not None:
            username = args['username']
            try:
                user = User.query.filter_by(username=username).first()
            except:
                return jsonify({
                    'code': '403',
                    'message': 'No this user',
                    })
            try:
                photo_path = Photo_Path(path=path['gen'], userid=user.id)
                db.session.add(photo_path)
                db.session.commit()
            except:
                return jsonify({
                    'code': '403',
                    'message': 'database something wrong',
                    })

        return jsonify({
            'code':'200',
            'wordlist': json.dumps(word_list),
            'pic_b64':gpic_b64,
            })
