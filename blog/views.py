from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import RedirectView
from braces.views import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy, reverse
import datetime
from .forms import LoginForm, PublicateConfirm, CreatePostForm, SubscribeConfirm
from .models import Post, Profile, ReadedPost

# Create your views here.


class CreatePost(CreateView):
    form_class = CreatePostForm
    template_name = 'posts/create_post.html'

    def get_success_url(self):
        return reverse('author_blog_list', args=(self.request.user.id,))

    def get_initial(self):
        initial = super(CreatePost, self).get_initial()
        initial = initial.copy()
        initial['author'] = self.request.user
        return initial

    def form_valid(self, form):
        form.data.author = self.request.user
        return super(CreatePost, self).form_valid(form)


class Subscribe(FormView):
    form_class = SubscribeConfirm
    template_name = 'authors/subscribe_confirm.html'
    success_url = reverse_lazy('authors')

    def form_valid(self, form):
        author_id = self.kwargs['author_id']
        user_id = self.request.user.id
        subscriber = Profile.objects.get(pk=user_id)
        author = Profile.objects.get(pk=author_id)
        author.profile_set.add(subscriber)
        author.save()
        return super(Subscribe, self).form_valid(form)


class Publicate(FormView):
    form_class = PublicateConfirm
    success_url = reverse_lazy('index')
    template_name = 'authors/post_publicate_confirm.html'

    def form_valid(self, form):
        public_post = Post.objects.get(pk=int(self.kwargs['pk']))
        public_post.published = datetime.datetime.now()
        public_post.save()
        return super(Publicate, self).form_valid(form)


class PostsListView(ListView):
    model = Post
    context_object_name = 'posts_list'
    queryset = Post.objects.exclude(published__isnull=True)
    template_name = 'posts/index.html'


class AuthorsListView(ListView):
    model = Profile
    context_object_name = 'authors_list'
    template_name = 'authors/authors_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorsListView, self).get_context_data(*args, **kwargs)
        context['user_profile'] = Profile.objects.get(pk=int(self.request.user.id))
        return context


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

    def get_context_data(self, *args, **kwargs):
        context = super(ViewPost, self).get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            post_id = self.kwargs['pk']
            readed, created = ReadedPost.objects.get_or_create(post_id=post_id,
                                user_id=user_id,
                                defaults={'post_id': post_id, 'user_id': user_id})
            if created:
                readed.save()
        return context


class AuthorBlogList(ListView):
    model = Post
    context_object_name = 'author_posts_list'
    pk_url_kwarg = "author_id"
    template_name = 'posts/author_posts_list.html'

    def get_queryset(self):
        author_id = int(self.kwargs['author_id'])
        return Post.objects.filter(author_id=author_id)

    def get_context_data(self, *args, **kwargs):
        context = super(AuthorBlogList, self).get_context_data(**kwargs)
        context['can_create'] = (int(self.kwargs['author_id']) == self.request.user.id)
        return context


class RibbonBlogList(ListView):
    """Отображение «моей ленты» (подписок)"""
    model = Post
    context_object_name = 'ribbon'
    template_name = 'posts/posts_ribbon.html'

    # def get_context_data(self, *args, **kwargs):
    #     context = super(RibbonBlogList, self).get_context_data(*args, **kwargs)
    #     return context


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
