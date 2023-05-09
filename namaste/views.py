from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from .forms import ContactMichModelForm

# Create your views here.

def base(request, *args, **kwargs):

    form = ContactMichModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some stuff

        obj.save()
    #     #print(form.cleaned_data)
    #     #data = form.cleaned_data
    #     #ContactInfo.objects.create(**data)
    #     # ContactInfo(**data) --> same as  obj = form.save(commit=False)
        form = ContactMichModelForm()
    #     # return HttpResponseRedirect("/success")
    #     # return redirect("/success")
    
    return render(request, 'namaste/base.html', {'form':form})


    