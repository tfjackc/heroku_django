from django.urls import path
from . import views
from django.views.generic import TemplateView

appname = 'namaste'

urlpatterns = [
    path('', views.base, name='base'),
]