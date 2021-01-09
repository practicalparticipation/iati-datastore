from flask import (abort, Blueprint, request, redirect, url_for)


builder = Blueprint('builder', __name__)


@builder.route('/<format>.csv')
@builder.route('/<format>/<grouping>.csv')
def builder_redirect(format, grouping=None):
    format_lookup = ['activity', 'transaction', 'budget']
    grouping_lookup = [None, 'by_sector', 'by_country']
    if format not in format_lookup:
        return abort(404)
    if grouping not in grouping_lookup:
        return abort(404)

    options = dict(request.args)
    if format != 'activity':
        options['format'] = format
    if grouping is not None:
        options['grouping'] = '/' + grouping

    return redirect(url_for('routes.homepage', **options))
