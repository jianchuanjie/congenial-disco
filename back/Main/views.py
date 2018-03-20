from flask import render_template, redirect, flash, url_for, request
from flask import current_app
from . import main
from ..forms import UploadForm
from .. import photos, docs
from WC.comeonpy3 import WCcreate
import os


@main.route('/uploads', methods=['GET', 'POST'])
def uoload_pic():
    form = UploadForm()
    gen_pic_url = None
    if form.validate_on_submit():
        photoname = photos.save(form.photo.data)
        photo_path = photos.path(photoname)
        docname = docs.save(form.doc.data)
        doc_path = docs.path(docname)
        gen_pic_path = WCcreate(doc_path=doc_path, mask_path=photo_path)
        gen_pic_url = photos.url(os.path.split(gen_pic_path)[1])
        print(photo_path, doc_path)
        print(gen_pic_url)
    return render_template('uploads.html', form=form, photo_url=gen_pic_url)
