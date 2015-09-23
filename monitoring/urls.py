from django.conf.urls import patterns, url
import core

urlpatterns = patterns('',
    url(r'', 'core.views.get_system'),
)
