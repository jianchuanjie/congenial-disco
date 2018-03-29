from flask import Blueprint

apiv = Blueprint('apiv', __name__)

from . import views
