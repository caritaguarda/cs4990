from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name="index"),
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name="detail"),
    url(r'^category/$', views.CategoryListView.as_view(), name="category"),
    url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(), name="categorydetail"),
    url(r'^commentsuccess/$', TemplateView.as_view(template_name='blogapp/commentsuccess.html'), name="commentsuccess"),
]
