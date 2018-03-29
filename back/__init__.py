from flask import Flask
from flask_uploads import UploadSet, configure_uploads, UploadSet
from flask_uploads import IMAGES, patch_request_class, DOCUMENTS
from flask_restful import Api


photos = UploadSet('photos', IMAGES)
docs = UploadSet('docs', ('doc', 'docx'))
api = Api()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # app.config.from_object('config')
    app.config.from_pyfile('config.py')

    configure_uploads(app, photos)
    configure_uploads(app, docs)
    patch_request_class(app)

    from .Main import main
    app.register_blueprint(main)
    from .Api_view import apiv
    api.init_app(apiv)
    app.register_blueprint(apiv)

    return app
