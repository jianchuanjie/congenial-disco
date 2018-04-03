from flask import render_template, redirect, flash, url_for, request
from flask import current_app, jsonify, abort
from .. import api
import os, time, hashlib, base64, imghdr
from flask_restful import Resource, reqparse
from WC.comeonpy3 import WC_app_create, readDocument, segment
from WC.comeonpy3 import FONTS_PATH, removeStopWords


types = (1, 2, 3)

colormaps = ('viridis', 'plasma', 'inferno', 'magma', 'Greys', 'Purples',
            'Blues', 'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd',
            'PuRd', 'RdPu', 'BuPu', 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn',
            'BuGn', 'YlGn', 'binary', 'gist_yarg', 'gist_gray', 'gray',
            'bone', 'pink', 'spring', 'summer', 'autumn', 'winter', 'cool',
            'Wistia', 'hot', 'afmhot', 'gist_heat', 'copper')

background_colors = ('white', 'black')

fonts = ('caiyun', 'kaiti', 'shaonv', 'xingkai', 'yasong', 'zhongsong', 'fan')


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


def from_doc_get_word_list(doc):
    doc = base64.b64decode(doc.encode())
    doc_name = get_name()
    doc_path = save_file(doc_name, doc, ext='doc')
    doc = readDocument(doc_path)
    segment_list = segment(doc)
    seg_list = removeStopWords(segment_list)
    return (doc_path, seg_list)


def from_photo_get_photo_path(photo):
    photo = base64.b64decode(photo.encode())
    photo_name = get_name()
    photo_path = save_file(photo_name, photo)
    return photo_path


def from_font_get_font_path(font):
    return os.path.join(FONTS_PATH, font + '.ttf')


def get_file_base64(path):
    f = open(path, 'rb').read()
    return  base64.b64encode(f)


def remove_files(paths):
    for path in paths.values():
        os.remove(path)


class Upload(Resource):
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
        self.parser.add_argument('font', type=str, default='fan')

    def get(self, text):
        return jsonify({'test':text})

    def post(self, text):
        args = self.parser.parse_args()
        # return jsonify({
        #     'type':args['type'],
        #     'photo':args['photo'],
        #     'doc':args['doc'],
        #     'txt':args['txt'],
        #     'url':args['url'],
        #     'max_words':args['max_words'],
        #     'background_color':args['background_color'],
        #     'max_font_size':args['max_font_size'],
        #     'colormap':args['colormap'],
        #     'font':args['font'],
        #     })
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


api.add_resource(Upload, '/api/<text>')
