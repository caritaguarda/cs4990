from django.conf.urls import url

from django.views.generic import TemplateView
from . import views

urlpatterns = [
   url(r'^$', views.CategoryListView.as_view(), name="categorylist"),
   url(r'^category/(?P<pk>[0-9]+)/$', views.CategoryDetailView.as_view(), name="categorydetail"),
   url(r'^category/add/$', views.CreateCategoryView.as_view(), name="addcategory"),
   url(r'^category/(?P<pk>[0-9]+)/update/$', views.UpdateCategoryView.as_view(), name="updatecategory"),
   url(r'^category/(?P<pk>[0-9]+)/delete/$', views.DeleteCategoryView.as_view(), name="deletecategory"),
   url(r'^delete/success/$', TemplateView.as_view(template_name="inventory/success.html"), name="deletesuccess"),
   url(r'^item/add/$', views.CreateItemView.as_view(), name="additem"),
   url(r'^item/(?P<pk>[0-9]+)/update/$', views.UpdateItemView.as_view(), name="itemupdate"),
   url(r'^item/(?P<pk>[0-9]+)/inc/$', views.increment, name="iteminc"),
   url(r'^item/(?P<pk>[0-9]+)/delete/$', views.DeleteItemView.as_view(), name="deleteitem"),
]