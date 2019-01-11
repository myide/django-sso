# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import User
from django.contrib import admin

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
