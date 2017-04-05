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
