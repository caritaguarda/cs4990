from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView, TemplateView
from django.core.urlresolvers import reverse_lazy, reverse
from viewsets import ModelViewSet
from django.db.models import Count
from .models import *
from django.forms.fields import ChoiceField

# Create your views here.

class DashboardView(TemplateView):
    template_name = 'crm/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['opportunity_list'] = Opportunity.objects.all().order_by('-create_date')[:5]
        context['reminder_list'] = Reminder.objects.all().exclude(completed = True).order_by('date')[:5]
        context['stage_list'] = User.objects.annotate(num_opp = Count('opportunity'))

        return context


class CallListView(ListView):
    model = CallLog

    def get_queryset(self):
        return CallLog.objects.order_by('-date')[:5]


class CallDetailView(DetailView):
    model = CallLog

class CallEditView(UpdateView):
    model = CallLog
    fields = ['opportunity', 'note']
    template_name = 'crm/calllog_edit.html'

    def get_success_url(self):

        return reverse('crm:calldetail', args=(self.object.pk,))


class CallAddView(CreateView):
    model = CallLog
    fields = ['opportunity', 'note']

    def get_success_url(self):
        return reverse('crm:calllist')

    def form_valid(self,form):
        call = form.save(commit=False)
        call.user = User.objects.filter(id=self.request.user.id)[0]
        call.save()

        return super(CallAddView, self).form_valid(form)


class CallDeleteView(DeleteView):
    model = CallLog
    success_url = reverse_lazy('crm:calllist')


class ContactListView(ListView):
    model = Contact

class ContactDetailView(DetailView):
    model = Contact


    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data()
        opportunities = []
        for opportunity in Opportunity.objects.all().filter(contact_id=self.object.pk):
            opportunities.append(opportunity)
        context['opportunity_list'] = opportunities
        return context


class ContactEditView(UpdateView):
    model = Contact
    fields = ['company', 'first_name', 'last_name', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', 'phone', 'email']

    def get_success_url(self):
        return reverse('crm:contactdetail', args=(self.object.pk,))


class ContactAddView(CreateView):
    model = Contact
    fields = ['first_name', 'last_name', 'phone', 'email', 'address1', 'address2', 'city', 'state', 'zipcode', 'country', 'company', ]
    success_url = reverse_lazy('crm:contactlist')


class ContactDeleteView(DeleteView):
    model = Contact
    success_url = reverse_lazy('crm:contactlist')



class CompanyListView(ListView):
    model = Company

class CompanyDetailView(DetailView):
    model = Company

class CompanyEditView(UpdateView):
    model = Company
    fields = ['name', 'website', 'phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country']

    def get_success_url(self):
        return reverse('crm:companydetail', args=(self.object.pk,))


class CompanyAddView(CreateView):
    model = Company
    fields = ['name', 'website', 'phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country']
    success_url = reverse_lazy('crm:companylist')


class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy('crm:companylist')


class CampaignListView(ListView):
    model = Campaign

class CampaignDetailView(DetailView):
    model = Campaign

    def get_context_data(self, **kwargs):
        context = super(CampaignDetailView, self).get_context_data(**kwargs)
        opportunity_list = []
        for opportunity in Opportunity.objects.all().filter(source = self.kwargs['pk']):
            opportunity_list.append(opportunity)
        context["opportunity_list"] = opportunity_list
        return context


class CampaignEditView(UpdateView):
    model = Campaign
    fields = ['name', 'description']

    def get_success_url(self):
        return reverse('crm:campaigndetail', args=(self.object.pk,))


class CampaignAddView(CreateView):
    model = Campaign
    fields = ['name', 'description']
    success_url = reverse_lazy('crm:campaignlist')

class ReportListView(ListView):
    model = Report
    ordering = 'name'



class StageListView(ListView):
    pass


class StageDetailView(DetailView):
    pass


class StageEditView(UpdateView):
    pass



class OpportunityListView(ListView):
    model = Opportunity



class OpportunityDetailView(DetailView):
    model = Opportunity

    def get_context_data(self, **kwargs):
        context = super(OpportunityDetailView, self).get_context_data()
        context["recent_calls"] = CallLog.objects.all().filter(opportunity = self.kwargs['pk'])[:5]
        return context


class OpportunityEditView(UpdateView):
    model = Opportunity
    fields = ['company', 'contact', 'value', 'stage', 'source']

    def get_success_url(self):
        return reverse('crm:opportunitydetail', args=(self.object.pk,))

    def form_valid(self, form):
        opportunity = form.save(commit=False)

        if opportunity.stage.value != self.get_object().stage.value:
            opportunity_stage = OpportunityStage()
            opportunity_stage.opportunity = opportunity
            opportunity_stage.stage = form.cleaned_data['stage']
            opportunity_stage.user = self.request.user
            opportunity_stage.save()

        opportunity.save()

        return super(OpportunityEditView, self).form_valid(form)


class OpportunityAddView(CreateView):
    model = Opportunity
    fields = ['company', 'contact', 'value', 'stage', 'source']
    success_url = reverse_lazy('crm:opportunitylist')

    def form_valid(self, form):
        opportunity = form.save(commit=False)
        opportunity.user = User.objects.filter(id = self.request.user.id)[0]
        opportunity.save()

        if opportunity.stage.value:
            opportunity_stage = OpportunityStage()
            opportunity_stage.opportunity = opportunity
            opportunity_stage.stage = form.cleaned_data['stage']
            opportunity_stage.user = self.request.user
            opportunity_stage.save()

        return super(OpportunityAddView, self).form_valid(form)



class OpportunityDeleteView(DeleteView):
    model = Opportunity
    success_url = reverse_lazy('crm:opportunitylist')


class ReminderListView(ListView):
    model = Reminder
    ordering = 'date'

    def get_queryset(self):
        queryset = Reminder.objects.all().filter(completed = False)
        return queryset


class ReminderDetailView(DetailView):
    model = Reminder

class ReminderCompleteView(ListView):
    model = Reminder
    template_name = 'crm/reminder_complete.html'

    def get_queryset(self):
        queryset = Reminder.objects.all().filter(completed = True)
        return queryset


class ReminderEditView(UpdateView):
    model = Reminder
    fields = ['opportunity','date','note','completed']
    success_url = reverse_lazy('crm:reminderlist')


class ReminderAddView(CreateView):
    model = Reminder
    fields = ['opportunity','date','note']
    success_url = reverse_lazy('crm:reminderlist')


class ReminderDeleteView(DeleteView):
    model = Reminder
    success_url = reverse_lazy('crm:remindercomplete')

