from os.path import join

from flask import Blueprint, redirect, current_app, \
    send_from_directory, Markup, url_for
import markdown
import markdown.extensions.tables

routes = Blueprint('routes', __name__, template_folder='templates')

@routes.route('/')
def homepage():
    return redirect(url_for('routes.docs', path='api/'))

@routes.route('/error')
def error():
    return redirect(url_for('routes.docs', path='api/error/'))

@routes.route('/docs/')
@routes.route('/docs/<path:path>')
def docs(path=''):
    folder = join('frontend', 'docs', 'dirhtml')
    if (path.endswith('/') or path==''):
        path += 'index.html'
    return send_from_directory(folder, path)

@routes.route('/favicon.ico')
def favicon():
    return send_from_directory(
        join('frontend', 'static'), 'favicon.ico')
