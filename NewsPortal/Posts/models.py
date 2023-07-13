from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.urls import reverse


#####################################################################################################################


class Author(models.Model):
    one_user = models.OneToOneField(User, on_delete=models.CASCADE)

    rating = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum("rating"))
        pRat = 0
        pRat += postRat.get("postRating")

        commentRat = self.one_user.comment_set.aggregate(commentRating=Sum("rating"))
        cRat = 0
        cRat += commentRat.get("commentRating")

        self.rating = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f"Автор {self.one_user}, " \
               f"Рейтинг {self.rating}"


########################################################################################################################

class Category(models.Model):
    name_category = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"Категория {self.name_category}"


########################################################################################################################

class Post(models.Model):
    article = 'AT'
    news = 'NW'
    TYPE = [(article, 'Статья'), (news, 'Новость')]

    many_author = models.ForeignKey(Author, on_delete=models.CASCADE)

    article_or_news = models.CharField(max_length=2, choices=TYPE, default=article)

    datetime = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(to='Category', on_delete=models.CASCADE)

    header = models.CharField(max_length=150)

    text = models.TextField()

    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    @property
    def preview(self):
        return self.text[:123] + "..."

    def get_news_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def get_articles_url(self):
        return reverse('articles_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.header}"


########################################################################################################################

# class PostCategory(models.Model):
#     many_post = models.ForeignKey(Post, on_delete=models.CASCADE)
#
#     many_category = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f"{self.many_category} к посту {self.many_post}"


########################################################################################################################

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)

    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)

    text = models.TextField()

    datetime = models.DateTimeField(auto_now_add=True)

    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"К посту {self.comment_post}, " \
               f"Автор комментария {self.comment_user}, " \
               f"Дата {self.datetime}"

########################################################################################################################
