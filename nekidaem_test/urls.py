"""nekidaem_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
# from django.views.generic import ListView
from blog import views
import blog.models as blog

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.PostsListView.as_view(model=blog.Post), name='index'),
    url(r'^authors/$', views.AutorsListView.as_view(model=blog.Profile), name='authors'),
    url(r'^author/(?P<pk>\d+)/$', views.AuthorDetails.as_view(model=blog.Profile), name='author'),
    url(r'^post/(?P<pk>\d+)/$', views.ViewPost.as_view(), name='view_post'),
    url(r'^blog/(?P<author_id>\d+)/$', views.AuthorBlogList.as_view(), name='author_blog_list'),
    url(r'^ribbon/$', views.RibbonBlogList.as_view(), name='ribbon'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogOutView.as_view(), name='logout'),
    url(r'^subscribe/(?P<author_id>\d+)/$', views.Subscribe, name='subscribe_this_author'),
    url(r'^publicate/(?P<pk>\d+)/$', views.Publicate.as_view(), name='publicate_post'),
]
