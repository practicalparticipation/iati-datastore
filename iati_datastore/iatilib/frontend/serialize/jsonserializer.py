from collections import OrderedDict
import datetime
from decimal import Decimal

from flask import json as jsonlib

import xmltodict
from flask_sqlalchemy import BaseQuery

from iatilib.model import (
    Activity, Organisation, Transaction, Participation, SectorPercentage,
    CountryPercentage, Budget
)
from iatilib import codelists


class JSONEncoder(jsonlib.JSONEncoder):
    TWOPLACES = Decimal(10) ** -2

    def default(self, o):
        if isinstance(o, BaseQuery):
            return o.all()
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, codelists.enum.EnumSymbol):
            return o.value
        if isinstance(o, Decimal):
            return str(o.quantize(self.TWOPLACES))
        if isinstance(o, Activity):
            if o.raw_json:
                return o.raw_json
            else:
                d = xmltodict.parse(o.raw_xml, attr_prefix='', cdata_key='text', strip_whitespace=False)
                d['iati-extra:version'] = o.version
                return d
        return super().default(o)


class DatastoreJSONEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Activity):
            return json_rep(o)
        return super().default(o)


def code(attr):
    if attr:
        return {
             "code": attr.value
             # "value": attr.value,
             # "description": attr.description
        }
    return None


def json_rep(obj):
    if isinstance(obj, Activity):
        return OrderedDict((
            ("iati-identifier", obj.iati_identifier),
            ("title", obj.title),
            ("description", obj.description),
            ("reporting-org", json_rep(obj.reporting_org)),
            ("license", obj.resource.dataset.license if obj.resource else None),
            ("version", obj.version),
            ("start-planned", obj.start_planned),
            ("end-planned", obj.end_planned),
            ("start-actual", obj.start_actual),
            ("end-actual", obj.end_actual),
            ("activity-website", list(obj.websites)),
            ("transaction", [json_rep(o) for o in obj.transactions]),
            ("participating-org", [json_rep(o) for o in obj.participating_orgs]),
            ("recipient-country", [json_rep(o) for o in obj.recipient_country_percentages]),
            ("sector", [json_rep(o) for o in obj.sector_percentages]),
            ("budget", {}),
            ("last-change", obj.last_change_datetime),

        ),)
    if isinstance(obj, Organisation):
        return {
            "ref": obj.ref,
            "name": obj.name,
        }
    if isinstance(obj, Transaction):
        return {
            "value": {
                "value-date": obj.value.date,
                "text": obj.value.amount,
                "currency": code(obj.value.currency),
            },
            "transaction-type": {"code": obj.type.value},
            "transaction-date": {"iso-date": obj.date},
            "flow-type": {"code": obj.flow_type},
            "finance-type": {"code": obj.finance_type},
            "aid-type": {"code": obj.aid_type},
            "disbursement-channel": {"code": obj.disbursement_channel},
            "tied-status": {"code": obj.tied_status}
        }
    if isinstance(obj, Participation):
        return {
            "organisation": json_rep(obj.organisation),
            "role": code(obj.role),
        }
    if isinstance(obj, CountryPercentage):
        return {
            "country": {
                "code": obj.country.value if obj.country else None,
                "name": obj.name,
            },
            "percentage": obj.percentage,
        }
    if isinstance(obj, SectorPercentage):
        return {
            "sector": code(obj.sector),
            "vocabulary": code(obj.vocabulary),
            "percentage": obj.percentage,
        }
    if isinstance(obj, Budget):
        return {
            "type": code(obj.type),
            "period-start": obj.period_start,
            "period-end": obj.period_end,
            "value": {
                "currency": obj.value_currency.value,
                "amount": str(obj.value_amount),
            }
        }
    return {}


class JSONSerializer:
    def __init__(self, encoder):
        self.encoder = encoder

    def __call__(self, pagination, wrapped=True):
        yield '{'
        if wrapped:
            yield jsonlib.dumps(
                OrderedDict((
                    ("ok", True),
                    ("total-count", pagination.total),
                    ("start", pagination.offset),
                    ("limit", pagination.limit),
                )))[1:-1] + ', '
        yield '"iati-activities": ['
        first = True
        for i in pagination.items:
            if first:
                first = False
            else:
                yield ', '
            yield jsonlib.dumps(i, cls=self.encoder)
        yield ']}'


json = JSONSerializer(JSONEncoder)
datastore_json = JSONSerializer(DatastoreJSONEncoder)
