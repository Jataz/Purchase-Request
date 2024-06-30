from django.contrib import admin
from django.contrib.auth.models import Permission
from myapp.models import Quotation

# Register your models here.
admin.site.register(Quotation)
admin.site.register(Permission)