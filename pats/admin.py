from django.contrib import admin
from django.forms.widgets import Textarea

# Register your models here.
from pats.models import ContactInfo, ContactMich

#admin.site.register(ContactInfo, admin.ModelAdmin)
#admin.site.register(ContactMich, admin.ModelAdmin)

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'submitted_at')

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContactInfoAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 36em;'
        form.base_fields['email'].widget.attrs['style'] = 'width: 36em;'
        form.base_fields['message'].widget = Textarea(attrs={'rows': 5, 'cols': 60, 'style': 'vertical-align: text-top;'})
        
        return form
    
@admin.register(ContactMich)
class ContactMichAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'submitted_at')

    def get_form(self, request, obj=None, **kwargs):
        form = super(ContactMichAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['name'].widget.attrs['style'] = 'width: 36em;'
        form.base_fields['email'].widget.attrs['style'] = 'width: 36em;'
        form.base_fields['message'].widget = Textarea(attrs={'rows': 5, 'cols': 60, 'style': 'vertical-align: text-top;'})
        
        return form
    
