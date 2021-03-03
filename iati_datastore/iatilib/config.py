import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'IATI_DATASTORE_DATABASE_URL', 'postgres:///iati-datastore')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False


# Due to a nasty OSX bug, we have to prevent checking system for proxies...
# https://wefearchange.org/2018/11/forkmacos.rst.html
# https://stackoverflow.com/a/53047403/11841218
os.environ['no_proxy'] = '*'
