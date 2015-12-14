from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView, TemplateView
from django.core.urlresolvers import reverse_lazy, reverse
from viewsets import ModelViewSet
from django.db.models import Count
from .models import *
from django.forms.fields import ChoiceField
from django.forms.models import modelform_factory
from bootstrap3_datetime.widgets import DateTimePicker


# Create your views here.
class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


class DashboardView(TemplateView):
    template_name = 'crm/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['opportunity_list'] = Opportunity.objects.all().order_by('-create_date')[:5]
        context['reminder_list'] = Reminder.objects.all().exclude(completed = True).order_by('date')[:5]
        context['stage_list'] = Stage.objects.annotate(num_opp = Count('opportunity'))
        context["opp_users"] = User.objects.filter(opportunitystage__stage__value = 100).annotate(num_opp=Count('opportunitystage'))[:5]


        return context


class SearchResultsView(TemplateView):
    template_name = 'crm/searchresults.html'

    def get_context_data(self, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        if not self.request.GET.get("q", None):
            return context
        search = self.request.GET['q']
        search_list = search.split(' ')
        contact_results = set()
        company_results = set()
        opportunities_results = set()
        reminder_results = set()
        call_results = set()
        for word in search_list:
            contacts = Contact.objects.filter(first_name__icontains = word)
            for contact in contacts:
                contact_results.add(contact)
            contacts = Contact.objects.filter(last_name__icontains = word)
            for contact in contacts:
                contact_results.add(contact)
            context['contacts'] = list(contact_results)

            companies = Company.objects.filter(name__icontains = word)
            for company in companies:
                company_results.add(company)
            for contact in contact_results:
                companies = Company.objects.filter(contact = contact)
                for c in companies:
                    company_results.add(c)
            context['companies'] = list(company_results)

            opportunities = Opportunity.objects.filter(description__icontains = word)
            for opportunity in opportunities:
                opportunities_results.add(opportunity)
            for company in company_results:
                opportunities = Opportunity.objects.filter(company = company)
                for o in opportunities:
                    opportunities_results.add(o)
            for contact in contact_results:
                opportunities = Opportunity.objects.filter(contact = contact)
                for o in opportunities:
                    opportunities_results.add(o)
            context['opportunities'] = list(opportunities_results)

            reminders = Reminder.objects.filter(note__icontains = word)
            for reminder in reminders:
                reminder_results.add(reminder)
            for opportunity in opportunities_results:
                reminders = Reminder.objects.filter(opportunity = opportunity)
                for r in reminders:
                    reminder_results.add(r)

            context['reminders'] = list(reminder_results)

            calls = CallLog.objects.filter(note__icontains = word)
            for call in calls:
                call_results.add(call)
            for opportunity in opportunities_results:
                calls = CallLog.objects.filter(opportunity = opportunity)
                for c in calls:
                    call_results.add(c)
            context['calls'] = list(call_results)

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


class CallAddView(ModelFormWidgetMixin, CreateView):
    model = CallLog
    fields = ['date', 'note']
    widgets = {
        'date': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": "false",
                                        "stepping": "15",
                                        "sideBySide": "true" })
    }

    def get_success_url(self):
        return reverse('crm:opportunitydetail', args=(self.kwargs['pk']))

    def form_valid(self,form):
        call = form.save(commit=False)
        call.user = User.objects.filter(id=self.request.user.id)[0]
        call.opportunity = Opportunity.objects.get(id = self.kwargs['pk'])
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


class StageDetailView(ListView):
    model = Stage
    template_name = 'crm/opportunity_by_stage.html'



class StageEditView(UpdateView):
    pass



class OpportunityListView(ListView):
    model = Opportunity



class OpportunityDetailView(DetailView):
    model = Opportunity

    def get_context_data(self, **kwargs):
        context = super(OpportunityDetailView, self).get_context_data()
        context["recent_calls"] = CallLog.objects.all().filter(opportunity = self.kwargs['pk']).order_by('-date')[:5]
        return context


class OpportunityEditView(UpdateView):
    model = Opportunity
    fields = ['company', 'contact', 'value', 'stage', 'source', 'description']

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

class AddOpportunityReminderView(ModelFormWidgetMixin, CreateView):
    model = Reminder
    template_name = 'crm/opportunity_reminder_form.html'
    fields = ['date', 'note']

    def get_success_url(self):
        return reverse('crm:opportunitydetail', args=(self.kwargs['pk'],))

    widgets = {
        'date': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                   "pickSeconds": "false",
                                    "stepping": "15",
                                    "sideBySide": "true" })
    }

    def form_valid(self, form):
        reminder = form.save(commit=False)
        reminder.opportunity = Opportunity.objects.get(id = self.kwargs['pk'])
        reminder.save()
        return super(AddOpportunityReminderView, self).form_valid(form)




class OpportunityAddView(CreateView):
    model = Opportunity
    fields = ['company', 'contact', 'value', 'stage', 'source', 'description']
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


class ReminderAddView(ModelFormWidgetMixin, CreateView):
    model = Reminder
    fields = ['opportunity','date','note']
    success_url = reverse_lazy('crm:reminderlist')

    widgets = {
    'date': DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                   "pickSeconds": "false",
                                    "stepping": "15",
                                    "sideBySide": "true" })
    }


class ReminderDeleteView(DeleteView):
    model = Reminder
    success_url = reverse_lazy('crm:remindercomplete')

