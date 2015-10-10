from django.conf.urls import patterns, url
from django.conf import settings
import core

urlpatterns = patterns('',
    url(settings.SECRET_URL, 'core.views.get_system'),
)
