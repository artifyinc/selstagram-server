#!/usr/bin/python
# -*- coding: utf-8 -*-
import getpass

from .local import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': getpass.getuser(),
        'NAME': 'selstagram',
        'ATOMIC_REQUESTS': True,
    }
}
