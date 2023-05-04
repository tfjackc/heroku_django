from django.contrib import admin

# Register your models here.
from pats.models import ContactInfo, ContactMich

admin.site.register(ContactInfo, admin.ModelAdmin)
admin.site.register(ContactMich, admin.ModelAdmin)