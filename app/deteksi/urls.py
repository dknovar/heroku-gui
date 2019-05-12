from django.conf.urls import url
import os
from . import views
from .views import FileView

urlpatterns = [
    url(r'^upload/$', FileView.as_view(), name='file-upload'),
    url(r'^$', views.index),
    
]
