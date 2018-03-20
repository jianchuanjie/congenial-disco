from flask import render_template, redirect, flash, url_for, request
from flask import current_app
from . import main
from ..forms import UploadForm
from .. import photos


@main.route('/uploads', methods=['GET', 'POST'])
def uoload_pic():
    form = UploadForm()
    file_url = None
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = photos.url(filename)
        print(file_url)
    return render_template('uploads.html', form=form, file_url=file_url)
