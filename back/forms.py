from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from . import photos, docs


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, 'Image only!'),
                                  FileRequired('File was empty!')])
    doc = FileField(validators=[FileAllowed(docs, 'docx needed'),
                                FileRequired('File was empty!')])
    submit = SubmitField('Upload')
