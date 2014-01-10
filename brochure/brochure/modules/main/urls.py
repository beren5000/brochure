from django.conf.urls import patterns, include, url


from brochure.modules.main.views import *

urlpatterns = patterns('',

    url(r'^$', brochure, name='home'),

)
