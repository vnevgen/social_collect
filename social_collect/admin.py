__author__ = 'vitaly'

from django.contrib import admin
from . import models

admin.site.register(models.Person)
admin.site.register(models.PersonAccount)