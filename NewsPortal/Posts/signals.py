from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(subscriptions__category=instance.category).values_list('email', flat=True)

    subject = f'Новый пост в категории {instance.category}'

    # Проверяем, является ли пост новостью или статьей.
    if instance.article_or_news == "NW":
        text_content = (
            f'Category: {instance.category}\n'
            f'Link: http://127.0.0.1:8000{instance.get_news_url()}'
        )
        html_content = (
            f'Category: {instance.category}<br>'
            f'<a href="http://127.0.0.1:8000{instance.get_news_url()}">'
            f'Link</a>'
        )
        for email in emails:
            msg = EmailMultiAlternatives(subject, text_content, None, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
