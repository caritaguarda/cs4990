from django.shortcuts import render
from .models import Profile, Post
from .forms import PostForm
from django.views.generic import ListView, UpdateView, CreateView, TemplateView, DetailView, FormView
from django.views.generic.detail import View, SingleObjectMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django import forms
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.

#homework:
# do list view of all recent posts, profile detail view,

class TweetListView(ListView):
    model = Post
    paginate_by = 5 #need to add pagination code
    queryset = Post.objects.all().order_by('-pub_date')



#class CreatePost(CreateView):
#    model = Post
#    fields = ['body']


#    def get_success_url(self):
#        return reverse('twitter:userposts', args=self.args)

class CreatePost(FormView):
    template_name = 'twitter/post_form.html'
    form_class = PostForm

    def form_valid(self, form):
        post = Post()
        post.body = form.cleaned_data['body']
        post.profile = Profile.objects.get(pk=self.kwargs['pk'])
        post.save()
        return super(CreatePost, self).form_valid(form)


    def get_success_url(self):
        return reverse('twitter:userposts', args = (self.kwargs['pk'],))


class ProfileDetailView(DetailView):
    model = Profile


class UserPosts(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(profile = self.kwargs['pk'])



class MyFeedView(ListView):
    model = Post
    paginate_by = 10
    template_name = "twitter/myfeed.html"

    def get_queryset(self):
        my_profile = Profile.objects.get_or_create(user=self.request.user)
        my_profile = self.request.user.profile_set.all()[0]
        profile_list = list(my_profile.following.all())
        profile_list.append(my_profile)
        return Post.objects.filter(profile__in = profile_list)



class UpdateProfile(UpdateView):
    model = Profile
    fields = ['picture', 'bio']

    def get_success_url(self):
        return reverse('twitter:profiledetail', args=(self.kwargs['pk'],))



class FollowFormView(SingleObjectMixin, View):
    model = Profile

    def post(self, request, *args, **kwargs):
        my_profile = request.user.profile_set.all()[0]
        try:
            my_profile.following.add(self.kwargs['pk'])
            my_profile.save()
        except:
            return HttpResponseRedirect(reverse('twitter:followsuccess', args= (self.kwargs['pk'], )))
        #return HttpResponseRedirect(reverse('microblog:followsuccess', kwargs = {'pk': self.get_object().pk}))
        #if request.is_ajax():
        #    return Http
        return HttpResponseRedirect(reverse('twitter:followsuccess', args = (self.kwargs['pk'], )))

class FollowSuccessView(DetailView):
    template_name = 'twitter/follow_success.html'
    model = Profile
