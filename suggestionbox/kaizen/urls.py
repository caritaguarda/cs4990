from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', login_required(views.IdeaListView.as_view()), name="idealist"),
    url(r'^(?P<pk>[0-9]+)/status/$', login_required(views.ChangeStatusView.as_view()), name="changestatus"),
    url(r'^newidea/$', login_required(views.CreateIdeaView.as_view()), name="newidea"),
    url(r'^category/$', login_required(views.CategoryListView.as_view()), name="categorylist"),
    url(r'^category/(?P<pk>[0-9]+)/$', login_required(views.CategoryDetailView.as_view()), name="categorydetail" ),
    url(r'^category/new/$', login_required(views.CreateCategory.as_view()), name="createcategory"),
    url(r'^idea/(?P<pk>[0-9]+)/$', views.IdeaDetailView.as_view(), name="ideadetail"),
    url(r'^comment/(?P<pk>[0-9]+)/$', views.CommentForm.as_view(), name="addcomment"),
]