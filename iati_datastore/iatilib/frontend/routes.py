from os.path import join

from flask import Blueprint, redirect, \
    send_from_directory, url_for


routes = Blueprint('routes', __name__, template_folder='templates')


@routes.route('/error/')
def error():
    return redirect(url_for('routes.docs', path='api/error/'))


@routes.route('/api/')
def api_latest():
    return redirect(url_for('api1.list_routes'))


@routes.route('/docs/')
@routes.route('/docs/<path:path>')
def docs(path=''):
    folder = join('frontend', 'docs', 'dirhtml')
    if path.endswith('/') or path == '':
        path += 'index.html'
    return send_from_directory(folder, path)


@routes.route('/')
@routes.route('/<path:path>')
def homepage(path=''):
    folder = join('frontend', 'querybuilder')
    if path.endswith('/') or path == '':
        path += 'index.html'
    return send_from_directory(folder, path)


@routes.route('/favicon.ico')
def favicon():
    return send_from_directory(
        join('frontend', 'static'), 'favicon.ico')
