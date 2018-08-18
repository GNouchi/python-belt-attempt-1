from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^travels$', views.travels),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addtrip$', views.addtrip),
    url(r'^newtrip$', views.newtrip),
    url(r'^show/(?P<id>\d)', views.show),
    url(r'^destroy/(?P<id>\d)', views.destroy),
    url(r'^join/(?P<id>\d)', views.join),
    url(r'^cancel/(?P<id>\d)', views.cancel),
    url(r'^$', views.index),
]