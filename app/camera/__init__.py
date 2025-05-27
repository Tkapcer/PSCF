from flask import Blueprint

camera = Blueprint('camera', __name__)

from . import routes