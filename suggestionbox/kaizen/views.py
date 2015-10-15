from django.shortcuts import render
from .models import Idea, Profile, Category, Comment
from django.views.generic import ListView, UpdateView, CreateView, TemplateView, DetailView, FormView
from django.core.urlresolvers import reverse


# Create your views here.
class IdeaListView(ListView):
    model = Idea

class IdeaDetailView(DetailView):
    model = Idea


class ChangeStatusView(UpdateView):
    model = Idea
    fields = ['status']
    template_name = "kaizen/changestatus.html"

    def get_success_url(self):
        return reverse('ideadetail', args=(self.object.pk,))

class CreateIdeaView(CreateView):
    model = Idea
    fields = ['title','description','category']

    def form_valid(self, form):
        idea = form.save(commit=False)

        #print self.__dict__
        idea.profile = Profile.objects.filter(user = self.request.user)[0]
        idea.save()
        return super(CreateIdeaView, self).form_valid(form)

    def get_success_url(self):
        return reverse('ideadetail', args=(self.object.pk,))


class CategoryListView(ListView):
    model = Category

class CategoryDetailView(DetailView):
    model = Category

class CreateCategory(CreateView):
    model = Category
    fields = ['title']

    def get_success_url(self):
        return reverse('categorydetail', args=(self.object.pk,))


class CommentForm(CreateView):
    model = Comment
    fields = ['comment_text', 'idea']

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.profile = Profile.objects.filter(user = self.request.user)[0]
        comment.save()
        return super(CommentForm, self).form_valid(form)


    def get_success_url(self):
        return reverse('ideadetail', args=(self.object.idea.id,))