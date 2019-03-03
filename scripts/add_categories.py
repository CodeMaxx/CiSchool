import os, sys
import json

sys_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'cischool')
sys.path.append(sys_path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'cischool.settings'

import django
django.setup()

from portal.models import UrlCategories

file = 'urlcategories.txt'

with open(file) as f:
	j = json.load(f)

for category in j["items"]:
	urlcat = UrlCategories.objects.create(name=category["name"], identity=category["id"], reputation="", link=category["links"]["self"])