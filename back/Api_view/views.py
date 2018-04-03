from flask import render_template, redirect, flash, url_for, request
from flask import current_app, jsonify, abort
from .. import api
import os, time, hashlib, base64, imghdr
from flask_restful import Resource, reqparse
from WC.comeonpy3 import WCcreate


colormaps = ('viridis', 'plasma', 'inferno', 'magma', 'Greys', 'Purples',
            'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd',
            'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn',
            'BuGn', 'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray',
            'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
            'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper')

backgroud_colors = ('white', 'black')


def get_name():
    return hashlib.md5(('wc' + str(time.time())).encode()).hexdigest()[:15]


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
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('photo', type=str, required=True)
        self.parser.add_argument('doc', type=str, required=True)
        self.parser.add_argument('max_words', type=int, default=2000)
        self.parser.add_argument('backgroud_color', default="white", choices=backgroud_colors)
        self.parser.add_argument('max_font_size', type=int, default=100)
        self.parser.add_argument('colormap', default="spring", choices=colormaps)

    def get(self, text):
        return jsonify({'test':text})

    def post(self, text):
        args = self.parser.parse_args()
        # return jsonify({
        #     'photo':args['photo'],
        #     'doc':args['doc'],
        #     'max_words':args['max_words'],
        #     'backgroud_color':args['backgroud_color'],
        #     'max_font_size':args['max_font_size'],
        #     'colormap':args['colormap'],
        #     })
        path = {}
        photo = base64.b64decode(args['photo'].encode())
        photo_name = get_name()
        path['photo'] = save_file(photo_name, photo)
        doc = base64.b64decode((args['doc'].encode()))
        doc_name = get_name()
        path['doc'] = save_file(doc_name, doc, ext='doc')
        path['gen'] = WCcreate(doc_path=path['doc'], mask_path=path['photo'],
            max_words=args['max_words'], backgroud_color=args['backgroud_color'],
            max_font_size=args['max_font_size'], colormap=args['colormap'])
        gpic_b64 = get_file_base64(path['gen']).decode()
        # remove_files(path)
        return jsonify({
            'code':'200',
            'where':text,
            # 'photo_path':path['photo'],
            # 'gpic_path':path['gen'],
            # 'photo':photo.decode()[:30],
            # 'doc_path':path['doc'],
            # 'doc':doc.decode()[:30],
            'pic_b64':gpic_b64,
            })


# def Test(Resource):
#     def __init__(self):
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument('test')
#         self.parser.add_argument('t2')

#     def get(self):
#         return jsonify({'test':'get_test'})

#     def post(self):
#         args = self.parse.parse_args()
#         if args['test'] is None:
#             abort(404)
#         return jsonify({'test':args['t2']+'\n'+args['test']})


api.add_resource(Upload, '/api/<text>')
# api.add_resource(Test, '/test/<t>')
