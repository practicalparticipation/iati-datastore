import sys
import os


PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, '/home/admin/iati-datastore/pyenv/lib/python3.6/site-packages')
sys.path.insert(0, PATH)

from iati_datastore.iatilib.wsgi import app as application
