# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import render_template, request, send_file, send_from_directory
from flask.helpers import url_for
from jinja2  import TemplateNotFound

# App modules
from app import app

# Backend
from backend import main
import io

puzzle = main.Sudoku()

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    try:
        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( path )
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404

@app.route('/', methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        in_memory_file = io.BytesIO()
        f.save(in_memory_file)
        puzzle.set_problem(in_memory_file)
        puzzle.solve()
        return render_template('index.html', processed=True, solved_sudoku=puzzle.solved, status=puzzle.status)

@app.route('/problem/')
def display_problem():
    byte_io = puzzle.get_problem()
    return send_file(byte_io, mimetype='image/jpeg', cache_timeout=0)

@app.route('/output/')
def display_output():
    byte_io = puzzle.get_output()
    return send_file(byte_io, mimetype='image/jpeg', cache_timeout=0)