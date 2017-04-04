#!/usr/bin/python
# -*- coding: utf-8 -*-

import getpass

from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': getpass.getuser(),
        'NAME': 'selstagram',
        'ATOMIC_REQUESTS': True,
    }
}

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/') + 'crawl.log',
        },
    },
    'loggers': {
        'selsta101.management.commands.crawl': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
