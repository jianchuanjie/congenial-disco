from flask import Flask
from flask_uploads import UploadSet, configure_uploads, UploadSet
from flask_uploads import IMAGES, patch_request_class, DOCUMENTS


photos = UploadSet('photos', IMAGES)
docs = UploadSet('docs', ('doc', 'docx'))


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_object('config')
    app.config.from_pyfile('config.py')

    configure_uploads(app, photos)
    configure_uploads(app, docs)
    patch_request_class(app)

    from .Main import main

    app.register_blueprint(main)

    return app
