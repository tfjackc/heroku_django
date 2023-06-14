from django.urls import path
from . import views
from django.views.generic import TemplateView
from portfolio.views import FoliumView

appname = 'portfolio'

urlpatterns = [
    path('', views.base, name='base'),
    path('foliumMap', FoliumView.as_view(), name='foliumMap'),
    path('propertyMap/', views.patsMapPage, name='patsMapPage'),
    path('jackcolpitt/', views.contact_create_view, name='contact_create_view'),
    path('jackcolpitt/resume/', views.resume, name='resume'),
    path('jhc/', views.jhc, name='jhc'),
    path('jhc/notebook/', views.notebook, name='notebook'),
    path('jhc/usgs_leaflet/', views.usgs, name='usgs')
]