from flask import (abort, Blueprint, request, redirect, url_for)


builder = Blueprint('builder', __name__)


@builder.route('/<breakdown>/')
@builder.route('/<breakdown>.<format>')
@builder.route('/<breakdown>/<grouping>.<format>')
def builder_redirect(breakdown, grouping=None, format='json'):
    breakdown_lookup = ['activity', 'transaction', 'budget']
    grouping_lookup = [None, 'by_sector', 'by_country']
    format_lookup = ['xml', 'json', 'csv']
    if breakdown not in breakdown_lookup:
        return abort(404)
    if grouping not in grouping_lookup:
        return abort(404)
    if format not in format_lookup:
        return abort(404)

    options = dict(request.args)
    if breakdown != 'activity':
        options['breakdown'] = breakdown
    if grouping is not None:
        options['grouping'] = '/' + grouping
    if format != 'xml':
        options['format'] = format

    return redirect(url_for('routes.homepage', **options))
