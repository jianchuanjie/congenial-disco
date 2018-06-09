from flask import Blueprint
from .. import api

apiv = Blueprint('apiv', __name__)

from .views import Upload
from .register import Register
from .login import Login
from .retrive import Retrive

api.add_resource(Upload, '/api/t')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Retrive, '/api/retrive')
