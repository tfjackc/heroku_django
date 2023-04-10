from django.urls import path
from . import views


appname = 'portfolio'

urlpatterns = [
    path('', views.base, name='base'),
    path('map', views.map, name='map'),
    path('jackcolpitt/', views.contact_create_view, name='contact_create_view'),
    path('jackcolpitt/notebook/', views.notebook, name='notebook'),
    path('jackcolpitt/resume/', views.resume, name='resume'),
]