# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u2236021/data/www/backend.goodcup.ru')
sys.path.insert(1, '/var/www/u2236021/data/www/backend.goodcup.ru/.venv/lib/python3.10/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'server.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
