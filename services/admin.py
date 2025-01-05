from django.contrib import admin
from .models import *

class ServiceAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}  

admin.site.register(Service, ServiceAdmin)