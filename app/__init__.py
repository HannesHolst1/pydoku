# -*- encoding: utf-8 -*-

# import Flask 
from flask import Flask

# Inject Flask magic
app = Flask(__name__)

# App Config
app.config.from_pyfile('../app-config.cfg')

# Import routing to render the pages
from app import views
