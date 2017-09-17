from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import RedirectView
from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy

from .forms import LoginForm, PublicateConfirm
from .models import Post, Profile

# Create your views here.


class Subscribe(FormView):
    pass


class MarkReaded(FormView):
    pass


class Publicate(FormView):
    form_class = PublicateConfirm
    success_url = reverse_lazy('index')
    template_name = 'authors/post_publicate_confirm.html'

    def form_valid(self, form):
        print('Publicate.form:', form)
        return super(LoginView, self).form_valid(form)


class PostsListView(ListView):
    model = Post
    context_object_name = 'posts_list'
    queryset = Post.objects.exclude(published__isnull=True)
    template_name = 'posts/index.html'


class AutorsListView(ListView):
    model = Profile
    context_object_name = 'authors_list'
    template_name = 'authors/authors_list.html'


class AuthorDetails(DetailView):
    model = Profile
    context_object_name = 'author_details'
    pk_url_kwarg = "pk"
    template_name = 'authors/author_details.html'


class ViewPost(DetailView):
    model = Post
    context_object_name = 'post'
    pk_url_kwarg = 'pk'
    template_name = 'posts/post_view.html'


class AuthorBlogList(ListView):
    model = Post
    context_object_name = 'author_posts_list'
    pk_url_kwarg = "author_id"
    template_name = 'posts/author_posts_list.html'

    def get_queryset(self):
        print('AuthorBlogList.get_queryset:', self.kwargs)
        author_id = int(self.kwargs['author_id'])
        return Post.objects.filter(author_id=author_id)

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorBlogList, self).get_context_data(**kwargs)
        print('AuthorBlogList.context:', context[self.context_object_name])
        return context


class RibbonBlogList(ListView):
    """Отображение «моей ленты» (подписок)"""
    model = Post
    context_object_name = 'ribbon'
    template_name = 'posts/posts_ribbon.html'

    def get_context_data(self, *args, **kwargs):
        context = super(RibbonBlogList, self).get_context_data(*args, **kwargs)
        print('RibbonBlogList.context:', context['ribbon'])
        # context['ribbon'] = Post.objects.filter(author in self.request.user.profile_set.all())
        return context


class LoginView(FormView):
    form_class = LoginForm
    success_url = reverse_lazy('index')
    template_name = 'authors/login.html'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class LogOutView(RedirectView):
    url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogOutView, self).get(request, *args, **kwargs)
