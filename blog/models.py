from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=1024, verbose_name='Название блога')
    subscribes = models.ManyToManyField('Profile', blank=True)  # Подписки

    def get_absolute_url(self):
        return '/author/%i/' % self.pk

    def __str__(self):
        return (f'{self.user.last_name} {self.user.first_name}: {self.blog_name}')

    # class Meta:
    #     ordering = ('first_name',)

User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


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

