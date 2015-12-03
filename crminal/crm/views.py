from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, DeleteView, TemplateView
from django.core.urlresolvers import reverse_lazy, reverse
from viewsets import ModelViewSet
from django.db.models import Count
from .models import *

# Create your views here.

class CallListView(ListView):
    model = CallLog

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

    success_url = reverse_lazy('crm:calllist')

    def form_valid(self,form):
        call = form.save(commit=False)
        call.user = User.objects.filter(id=self.request.user.id)[0]
        call.save()

        return super(CallAddView, self).form_valid(form)


class CallDeleteView(DeleteView):
    model = CallLog
    success_url = reverse_lazy('crm:calllist')

class StageViewSet(ModelViewSet):
    model = Stage
    fields = ['name', 'description']

class CompanyViewSet(ModelViewSet):
    model = Company


class ContactViewSet(ModelViewSet):
    model = Contact

class OpportunityViewSet(ModelViewSet):
    model = Opportunity

class CampaignViewSet(ModelViewSet):
    model = Campaign

class ReminderViewSet(ModelViewSet):
    model = Reminder

class DashboardView(TemplateView):
    template_name = 'crm/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['opportunity_list'] = Opportunity.objects.all().order_by('-create_date')[:5]
        context['reminder_list'] = Reminder.objects.all().exclude(completed = True).order_by('date')[:5]
        context['stage_list'] = User.objects.annotate(num_opp = Count('opportunity'))

        return context


