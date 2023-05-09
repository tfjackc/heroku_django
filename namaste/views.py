from django.shortcuts import render
from django.http import HttpResponse
import json
import requests

# Create your views here.

def base(request):

    return render(request, 'namaste/base.html')

    