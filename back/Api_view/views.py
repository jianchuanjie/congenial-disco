from flask import render_template, redirect, flash, url_for, request
from flask import current_app, jsonify
from .. import api
import os, time, hashlib, base64, imghdr
from flask_restful import Resource, reqparse
from WC.comeonpy3 import WCcreate


parser = reqparse.RequestParser()
parser.add_argument('photo')
parser.add_argument('doc')


def get_name():
    return hashlib.md5(('admin' + str(time.time())).encode()).hexdigest()[:15]


def save_file(name, file, ext=None):
    if ext is None:
        ext = imghdr.what(None, file)
    if ext is None:
        return None

    s_path = os.path.join(os.getcwd(), 'file', name+'.'+ext)
    f = open(s_path, 'wb')
    f.write(file)
    f.close()
    return s_path


def get_file_base64(path):
    f = open(path, 'rb').read()
    return  base64.b64encode(f)


def remove_files(paths):
    for path in paths.values():
        os.remove(path)


class Upload(Resource):
    def get(self, text):
        return jsonify({'test':text})

    def post(self, text):
        args = parser.parse_args()
        path = {}
        photo = base64.b64decode(args['photo'].encode())
        photo_name = get_name()
        path['photo'] = save_file(photo_name, photo)
        doc = base64.b64decode((args['doc'].encode()))
        doc_name = get_name()
        path['doc'] = save_file(doc_name, doc, ext='doc')
        path['gen'] = WCcreate(doc_path=path['doc'], mask_path=path['photo'])
        gpic_b64 = get_file_base64(path['gen']).decode()
        # remove_files(path)
        return jsonify({
            'code':'200',
            'where':text,
            'photo_path':path['photo'],
            'gpic_path':path['gen'],
            # 'photo':photo.decode()[:30],
            'doc_path':path['doc'],
            # 'doc':doc.decode()[:30],
            'pic_b64':gpic_b64,
            })


api.add_resource(Upload, '/api/<text>')
