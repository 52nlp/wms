#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request
import os, json, re, urllib, markdown

from .publications import publications
from .corpus import corpus

# Import constants
# import app.helpers.methods as methods

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

# Define the WSGI application object
app = Flask(__name__, instance_relative_config=True)

# Configurations that use app
# application = app # our hosting requires application in passenger_wsgi

app.register_blueprint(publications, url_prefix='/publications')
app.register_blueprint(corpus, url_prefix='/corpus')

# Configurations
app.config.from_object('config')
app.config.from_pyfile('config.py')

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/todo')
def todo():
	return render_template('todo.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/guide')
def guide():
	breadcrumbs = [{'link': '/guide', 'label': 'Guide'}]
	return render_template('guide.html', breadcrumbs=breadcrumbs)

@app.route('/schema')
def schema():
	breadcrumbs = [{'link': '/schema', 'label': 'Manifest Schema Documentation'}]
	f = urllib.request.urlopen('https://github.com/whatevery1says/manifest/raw/master/we1s-manifest-schema-1.1.md')
	md = f.read().decode('utf-8')	
	html = markdown.markdown(md, ['markdown.extensions.extra'])
	html = html.replace('<h1>WhatEvery1Says Schema</h1>', '')
	# Need to inject internal links in contents and elsewhere, as they are not 
	# carried over from GitHub.
	return render_template('schema.html', html=html, breadcrumbs=breadcrumbs)

# Error handlers.

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''