from django.contrib.auth.models import User
from django.db import models

from Posts.models import Category


class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    def __str__(self):
        return f"{self.user} подписан на {self.category}"
