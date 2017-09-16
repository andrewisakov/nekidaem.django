from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
# from braces.views import LoginRequiredMixin, GroupRequiredMixin

from .models import Post, Profile

# Create your views here.


class PostsListView(ListView):
    model = Post
    context_object_name = 'posts_list'
    queryset = Post.objects.exclude(published__isnull=True)
    template_name = 'posts/index.html'


class AutorsListView(ListView):
    model = Profile
    context_object_name = 'authors_list'
    # queryset = Profile.objects.all()
    template_name = 'authors/authors_list.html'


class AuthorDetails(DetailView):
    model = Profile
    context_object_name = 'author_details'
    # queryset = Profile.get
    pk_url_kwarg = "pk"
    template_name = 'authors/author_details.html'
