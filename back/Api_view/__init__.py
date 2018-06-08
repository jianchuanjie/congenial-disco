from flask import Blueprint
from .. import api

apiv = Blueprint('apiv', __name__)

from .views import Upload
from .register import Register

api.add_resource(Upload, '/api/<text>')
api.add_resource(Register, '/api/register')
