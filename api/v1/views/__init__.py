#!/usr/bin/python3
"""Create app_views Blueprint"""

from flsk import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.places import *
from api.v1.views.users import *
from api.v1.views.amenities import *
from api.v1.views.states import *
from api.v1.views.index import *
