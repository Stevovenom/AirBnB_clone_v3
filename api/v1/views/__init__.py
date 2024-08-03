#!/usr/bin/python3
"""Create app_views Blueprint"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__)

from api.v1.views.index import *
