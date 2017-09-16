from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=1024, verbose_name='Название блога')
    subscribes = models.ManyToManyField('Profile')


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


# class Subscribe(models.Model):
#     author = models.OneToOneField(Profile, related_name='user', primary_key=True)
#     user = models.OneToOneField(Profile, related_name='user', primary_key=True)


class Post(models.Model):
    title = models.CharField(verbose_name='Заголовок', max_length=256)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    published = models.DateTimeField(blank=True, verbose_name='Опубликовано')
    content = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(Profile)

    class Meta:
        ordering = ('-published',)


class ReadedPost(models.Model):
    post = models.OneToOneField(Post)
    user = models.ForeignKey('Profile')
    readed = models.DateTimeField(blank=True)

