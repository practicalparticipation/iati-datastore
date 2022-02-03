from datetime import datetime

from lxml import etree as ET

from .csv import (
    csv, csv_activity_by_country, csv_activity_by_sector,
    transaction_csv, csv_transaction_by_country, csv_transaction_by_sector,
    budget_csv, csv_budget_by_country, csv_budget_by_sector,
    xlsx, xlsx_activity_by_country, xlsx_activity_by_sector,
    transaction_xlsx, xlsx_transaction_by_country, xlsx_transaction_by_sector,
    budget_xlsx, xlsx_budget_by_country, xlsx_budget_by_sector,
)
from .jsonserializer import json, datastore_json


def xml(pagination, wrapped=True):
    generated_datetime = datetime.now().isoformat()
    if wrapped:
        yield """<result xmlns:iati-extra="https://datastore.codeforiati.org/ns">
      <ok>True</ok>
      <iati-activities generated-datetime="{generated_datetime}">
        <query>
          <total-count>{total}</total-count>
          <start>{offset}</start>
          <limit>{limit}</limit>
        </query>""".format(
        total=pagination.total,
        offset=pagination.offset,
        limit=pagination.limit,
        generated_datetime=generated_datetime)
    else:
        yield """<iati-activities xmlns:iati-extra="https://datastore.codeforiati.org/ns" generated-datetime="{generated_datetime}">""".format(
            generated_datetime=generated_datetime)
    for activity in pagination.items:
        if activity.version:
            # This should always work, as the first element in the raw_xml should always be iati-activity
            # And is lower overhead than using a proper XML parser again here
            yield str(activity.raw_xml.replace('<iati-activity', '<iati-activity iati-extra:version="{}"'.format(activity.version), 1))
        else:
            yield str(activity.raw_xml)
    yield "</iati-activities>"
    if wrapped:
        yield "</result>"
