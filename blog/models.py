from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import mail


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blog_name = models.CharField(max_length=1024, verbose_name='Название блога')
    subscribes = models.ManyToManyField("self", blank=True, symmetrical=False)  # Подписки

    def get_absolute_url(self):
        return '/author/%i/' % self.pk

    def __str__(self):
        return (f'{self.user.last_name} {self.user.first_name}: {self.blog_name}')


User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])


class Post(models.Model):
    title = models.CharField(max_length=256, verbose_name='Заголовок')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    published = models.DateTimeField(blank=True, null=True, verbose_name='Опубликовано')
    content = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(Profile, related_name='author', verbose_name='Автор')

    def get_absolute_url(self):
        return '/post/%i/' % self.pk

    def __str__(self):
        return f'{self.title}:{self.created}:{self.published}:{self.author}'

    class Meta:
        ordering = ('-published',)


@receiver(post_save, sender=Post, dispatch_uid='update_post_blog')
def update_post(sender, instance, **kwargs):
    sender_profile = Profile.objects.get(pk=instance.author_id)
    from_email = sender_profile.user.email
    message = f'Пользователь {sender_profile.user.first_name} {sender_profile.user.last_name} разместил/изменил запись в своём блоге.'
    subject = f'Новая/изменённая запись в блоге {sender_profile.user.first_name} {sender_profile.user.last_name}'
    recipient_list = [profile.user.email for profile in sender_profile.profile_set.all()]
    # Пока забьём...
    # connection = mail.get_connection()
    # print('models.update_post:', connection)
    # send_mail(subject, message, from_email, recipient_list,)
    # connection.send_messages([mail.EmailMessage(subject, message, from_email, recipient_list,),])
    # connection.close()
    # Не пошло. По уму тут асинхронка нужна...


class ReadedPost(models.Model):
    post = models.OneToOneField(Post)
    user = models.ForeignKey(Profile)
    readed = models.DateTimeField(auto_now_add=True, verbose_name='Прочитано')

    class Meta:
        unique_together = (('post', 'user'),)

