
"""twittersite URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView



urlpatterns = [
    url(r'^$', views.TweetListView.as_view(), name="tweetlist"),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileDetailView.as_view(), name="profiledetail"),
    url(r'^myfeed/$', login_required(views.MyFeedView.as_view()), name="myfeed"),
    url(r'^profile/(?P<pk>\d+)/addpost/$', login_required(views.CreatePost.as_view()), name="createpost"),
    url(r'^profile/(?P<pk>\d+)/posts/$', login_required(views.UserPosts.as_view()), name="userposts"),
    url(r'^profile/(?P<pk>\d+)/follow/$', login_required(views.FollowFormView.as_view()), name="follow"),
    url(r'^profile/(?P<pk>\d+)/follow/success/$', login_required(views.FollowSuccessView.as_view()), name="followsuccess"),
    url(r'^profile/(?P<pk>\d+)/update', login_required(views.UpdateProfile.as_view()), name="updateprofile"),

] 
