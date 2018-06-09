from flask import Blueprint
from .. import api

apiv = Blueprint('apiv', __name__)

from .views import Upload
from .register import Register
from .login import Login

api.add_resource(Upload, '/api/<text>')
api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
