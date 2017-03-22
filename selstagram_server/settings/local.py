#!/usr/bin/python
# -*- coding: utf-8 -*-

from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

#HC's local test environment
ALLOWED_HOSTS = ["192.168.0.2"]
