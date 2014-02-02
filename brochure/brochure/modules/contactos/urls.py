from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from brochure.modulos.contactos.views import *
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', contactos , name='contactos'),
)
