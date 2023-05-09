from django import forms 
from pats.models import ContactMich

class ContactMichForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    message = forms.CharField()

class ContactMichModelForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = ContactMich
        fields = [
            'name',
            'email',
            'message',
        ]