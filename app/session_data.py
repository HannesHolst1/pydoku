import os, time
from app import app

def clean():
    now = time.time()
    path = app.config['SESSION_FILE_DIR']
    lifetime = app.config['CLEAN_SESSION_FILES_AFTER']

    for filename in os.listdir(path):
        if os.path.getmtime(os.path.join(path, filename)) < now - lifetime:
            if os.path.isfile(os.path.join(path, filename)):
                os.remove(os.path.join(path, filename))