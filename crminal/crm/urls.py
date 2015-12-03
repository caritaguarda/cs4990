"""crminal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from viewsets import ModelViewSet

from views import *


urlpatterns = [
    url(r'^call/all/$', login_required(CallListView.as_view()), name="calllist" ),
    url(r'^call/(?P<pk>\d+)/$', login_required(CallDetailView.as_view()), name="calldetail"),
    url(r'^call/(?P<pk>\d+)/edit/$', login_required(CallEditView.as_view()), name="calledit"),
    url(r'^call/add/$', login_required(CallAddView.as_view()), name="calladd"),
    url(r'^call/(?P<pk>\d+)/delete/$', login_required(CallDeleteView.as_view()), name="calldelete"),
    url(r'^dashboard/$', login_required(DashboardView.as_view()), name="dashboard"),
    url('', include(ModelViewSet(Stage).urls)),
    url('', include(ModelViewSet(Company).urls)),
    url('', include(ModelViewSet(Contact).urls)),
    url('', include(ModelViewSet(Opportunity).urls)),
    url('', include(ModelViewSet(Campaign).urls)),
    url('', include(ModelViewSet(Reminder).urls)),





]
