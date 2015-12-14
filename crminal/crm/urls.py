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
    url(r'^$', login_required(DashboardView.as_view()), name="dashboard"),

    url(r'^call/all/$', login_required(CallListView.as_view()), name="calllist" ),
    url(r'^call/(?P<pk>\d+)/$', login_required(CallDetailView.as_view()), name="calldetail"),
    url(r'^call/(?P<pk>\d+)/edit/$', login_required(CallEditView.as_view()), name="calledit"),
    url(r'^call/add/(?P<pk>\d+)/$', login_required(CallAddView.as_view()), name="calladd"),
    url(r'^call/(?P<pk>\d+)/delete/$', login_required(CallDeleteView.as_view()), name="calldelete"),

    url(r'^search/$', login_required(SearchResultsView.as_view()), name="search"),

    url(r'^opportunity/all/$', login_required(OpportunityListView.as_view()), name="opportunitylist" ),
    url(r'^opportunity/add/$', login_required(OpportunityAddView.as_view()), name="opportunityadd"),
    url(r'^opportunity/(?P<pk>\d+)/$', login_required(OpportunityDetailView.as_view()), name="opportunitydetail"),
    url(r'^opportunity/(?P<pk>\d+)/edit/$', login_required(OpportunityEditView.as_view()), name="opportunityedit"),
    url(r'^opportunity/(?P<pk>\d+)/delete/$', login_required(OpportunityDeleteView.as_view()), name="opportunitydelete"),
    url(r'^opportunity/stage/$', login_required(StageDetailView.as_view()), name="stagedetail"),
    url(r'^opportunity/(?P<pk>\d+)/reminder/$', login_required(AddOpportunityReminderView.as_view()), name="opportunityreminder"),


    url(r'^contact/all/$', login_required(ContactListView.as_view()), name="contactlist" ),
    url(r'^contact/add/$', login_required(ContactAddView.as_view()), name="contactadd"),
    url(r'^contact/(?P<pk>\d+)/$', login_required(ContactDetailView.as_view()), name="contactdetail"),
    url(r'^contact/(?P<pk>\d+)/edit/$', login_required(ContactEditView.as_view()), name="contactedit"),
    url(r'^contact/(?P<pk>\d+)/delete/$', login_required(ContactDeleteView.as_view()), name="contactdelete"),
    
    url(r'^company/all/$', login_required(CompanyListView.as_view()), name="companylist" ),
    url(r'^company/add/$', login_required(CompanyAddView.as_view()), name="companyadd"),
    url(r'^company/(?P<pk>\d+)/$', login_required(CompanyDetailView.as_view()), name="companydetail"),
    url(r'^company/(?P<pk>\d+)/edit/$', login_required(CompanyEditView.as_view()), name="companyedit"),
    url(r'^company/(?P<pk>\d+)/delete/$', login_required(CompanyDeleteView.as_view()), name="companydelete"),
    
    url(r'^reports/$', login_required(ReportListView.as_view()), name="reports" ),
    
    url(r'^reminder/all/$', login_required(ReminderListView.as_view()), name="reminderlist" ),
    url(r'^reminder/add/$', login_required(ReminderAddView.as_view()), name="reminderadd"),
    url(r'^reminder/(?P<pk>\d+)/edit/$', login_required(ReminderEditView.as_view()), name="reminderedit"),
    url(r'^reminder/(?P<pk>\d+)/delete/$', login_required(ReminderDeleteView.as_view()), name="reminderdelete"),
    url(r'^reminder/complete/$', login_required(ReminderCompleteView.as_view()), name="remindercomplete"),


    url(r'^stage/all/$', login_required(StageListView.as_view()), name="stagelist" ),
    url(r'^stage/(?P<pk>\d+)/edit/$', login_required(StageEditView.as_view()), name="stageedit"),


    url(r'^campaign/all/$', login_required(CampaignListView.as_view()), name="campaignlist" ),
    url(r'^campaign/add/$', login_required(CampaignAddView.as_view()), name="campaignadd"),
    url(r'^campaign/(?P<pk>\d+)/$', login_required(CampaignDetailView.as_view()), name="campaigndetail"),
    url(r'^campaign/(?P<pk>\d+)/edit/$', login_required(CampaignEditView.as_view()), name="campaignedit"),


]
