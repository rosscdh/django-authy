# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

from .views import HoldingPageView, ProfileView


urlpatterns = patterns('',
    url(r'^holding/$', HoldingPageView.as_view(), name='holding'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
)
