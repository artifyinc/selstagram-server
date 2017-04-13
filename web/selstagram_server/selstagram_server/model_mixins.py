#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models


class StringHelperModelMixin(object):
    def __str__(self):
        return str(self.id)

    def field_list_to_string(self, field_list=[]):
        return_string = str(self.id) + ': '
        for string in field_list:
            return_string += str(string) + ', '

        return return_string[:-2]


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True