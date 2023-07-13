from celery import shared_task
import time
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail

from Posts.models import Post


@shared_task
def send_notification():
    time.sleep(10)

    # Получение первого элемента из списка постов
    url_news = Post.objects.filter(article_or_news__istartswith="NW").values().last()

    # Получение почтового адреса пользователей
    emails = User.objects.all().values_list('email', flat=True)

    subject = f'Новый пост {url_news["header"]}'

    text_content = (
        f'Новый пост\n'
        f'Ссылка: http://127.0.0.1:8000/news/{url_news["id"]}'
    )
    html_content = (
        f'<p>Новый пост</p>\n'
        f'<a href="http://127.0.0.1:8000/news/{url_news["id"]}">Ссылка</a>'
    )
    for email in emails:
        # Отправка письма пользователю.
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def send_last_news():
    # Получение первых 7 новостных постов из базы данных.
    only_news = Post.objects.filter(article_or_news__istartswith="NW").values()[:7]

    # Получение почтового адреса пользователей
    emails = User.objects.all().values_list('email', flat=True)

    for email in emails:
        send_mail(
            subject=f'Посты за эту неделю',
            message='\n'.join(['{}\n {}\n http://127.0.0.1:8000/news/{}\n'.format(
                _content["header"][:10] + "...",
                _content["text"][:30] + "...",
                _content["id"]) for _content in only_news]),
            from_email=None,
            recipient_list=[email],
        )
