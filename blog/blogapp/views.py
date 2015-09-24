from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect

from .models import Post, Comment, Category
from .forms import CommentForm

class IndexView(generic.ListView):
    template_name = 'blogapp/index.html'
    model = Post
    

    def get_queryset(self):
        #in order to only show the most recent 5 posts:
        return Post.objects.order_by('-pub_date')[:10]

class CategoryListView(generic.ListView):
    template_name = 'blogapp/category.html'
    model = Category
    

class PostDetailView(generic.DetailView):
    model = Post
    success_url = reverse_lazy('blogapp:commentsuccess')
    
    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context["form"] = CommentForm
        return context
        
    def form_valid(self, form):
        #add a comment

        comment = Comment()
        comment.person = form.cleaned_data['name']
        comment.comment_text = form.cleaned_data['comment']
        comment.post = form.cleaned_data['post']
        comment.save()
        
        return super(PostDetailView, self).form_valid(form)

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'blogapp/categorydetail.html'

class CommentFormView(FormView):
    form_class = CommentForm
    template_name = 'blogapp/commentform.html'
    success_url = reverse_lazy('blogapp:commentsuccess')
    

    
    
    #def get_context_data(self):
        #context = super(PostDetailView,self).get_context_data()
        #context.update({"comment_list": self.get_object().comment_set.all()})
        #context.update({"comment_list": Comment.objects.filter(post__pk = self.kwargs.get('pk'))})
        #return context
