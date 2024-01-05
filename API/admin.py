from django.contrib import admin
from .models import *


@admin.register(WhitelistRequest)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["user","domain", "addresses", "status"]

