from django.urls import path
from . import views
from django.views.generic import TemplateView
from portfolio.views import FoliumView

appname = 'portfolio'

urlpatterns = [
    path('', views.base, name='base'),
    path('map', FoliumView.as_view()),
    path('jackcolpitt/', views.contact_create_view, name='contact_create_view'),
    path('jackcolpitt/notebook/', views.notebook, name='notebook'),
    path('jackcolpitt/resume/', views.resume, name='resume'),
]