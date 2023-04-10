from django.shortcuts import render, redirect
from pats.models import ContactInfo
from django.http import HttpResponse, HttpResponseRedirect
import json
import requests
from .forms import ContactModelForm
# Create your views here.

def resume(request):
    return render(request, 'portfolio/resume.html')

def mainpage(request):
    
    return render(request, 'portfolio/mainpage.html')

def map(request):
    
    return render(request, 'portfolio/map.html')

def base(request):
    
    return render(request, 'portfolio/base.html')

def notebook(request):

    return render(request, 'portfolio/notebook.html')

def contact_create_view(request, *args, **kwargs):

    form = ContactModelForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        # do some stuff

        obj.save()
    #     #print(form.cleaned_data)
    #     #data = form.cleaned_data
    #     #ContactInfo.objects.create(**data)
    #     # ContactInfo(**data) --> same as  obj = form.save(commit=False)
        form = ContactModelForm()
    #     # return HttpResponseRedirect("/success")
    #     # return redirect("/success")
    
    return render(request, "portfolio/mainpage.html", {'form':form})



    