from django.urls import path
from .views import (AllPost, NewsList, NewsDetail, ArticleList, ArticleDetail, Search, NWCreate, NWEdit, ATCreate,
                    ATEdit, PostDel)

urlpatterns = [
    path('portal/', AllPost.as_view(), name="allpost"),

    path('news/', NewsList.as_view(), name="news"),
    path('news/<int:pk>', NewsDetail.as_view(), name="news_detail"),
    path('articles/', ArticleList.as_view(), name="article"),
    path('articles/<int:pk>', ArticleDetail.as_view(), name="articles_detail"),

    path('search/', Search.as_view()),

    path('news/create/', NWCreate.as_view(), name="news_create"),
    path('news/<int:pk>/edit/', NWEdit.as_view(), name="news_edit"),
    path('news/<int:pk>/delete/', PostDel.as_view(), name="news_delete"),

    path('articles/create/', ATCreate.as_view(), name="articles_create"),
    path('articles/<int:pk>/edit/', ATEdit.as_view(), name="articles_edit"),
    path('articles/<int:pk>/delete/', PostDel.as_view(), name="articles_delete"),
]
