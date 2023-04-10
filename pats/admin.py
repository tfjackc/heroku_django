from django.contrib import admin

# Register your models here.
from pats.models import ContactInfo

admin.site.register(ContactInfo, admin.ModelAdmin)