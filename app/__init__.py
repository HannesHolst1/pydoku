# -*- encoding: utf-8 -*-

# import Flask 
from flask import Flask

# Inject Flask magic
app = Flask(__name__)

# App Config - the minimal footprint
app.config['TESTING'   ] = True 
app.config['SECRET_KEY'] = 'S#perS3crEt_JamesBond'
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024
app.config['DEMOFILE_PATH'] = './backend/test_files/'
app.config['DEMOFILE_MASK'] = 'test*.jpg' 
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'
app.config['CLEAN_SESSION_FILES_AFTER'] = 300 # 5 minutes

# Import routing to render the pages
from app import views
