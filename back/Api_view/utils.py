import hashlib, base64, time, imghdr

'''
some mess functions and choices for Upload arguments
'''

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
    try:
        f = open(path, 'rb').read()
        return  base64.b64encode(f)
    except:
        return None


def remove_files(paths):
    for path in paths.values():
        os.remove(path)
