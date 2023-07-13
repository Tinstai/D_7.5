from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.urls import reverse_lazy

from .filters import PostFilter
from .forms import NWForm, ATForm
from .models import Post
from Cron.tasks import send_notification


# ----------------------------------------------------------------------------------------------------------------------

# Используется для отображения всех сообщений из базы данных.
class AllPost(ListView):
    model = Post
    ordering = 'datetime'
    template_name = 'flatpages/all_post.html'
    context_object_name = 'ALL'
    paginate_by = 10


########################################################################################################################

# Он используется для отображения всех новостей из базы данных.
class NewsList(ListView):
    model = Post
    ordering = 'datetime'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10


# Отображающее всех статьей из базы данных.
class ArticleList(ListView):
    model = Post
    ordering = 'datetime'
    template_name = 'flatpages/articles.html'
    context_object_name = 'articles'
    paginate_by = 10


########################################################################################################################

class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'new'


class ArticleDetail(DetailView):
    model = Post
    template_name = 'flatpages/article.html'
    context_object_name = 'article'


########################################################################################################################

# Представление на основе классов, которое используется для поиска сообщений в базе данных.
class Search(ListView):
    model = Post
    ordering = 'datetime'
    template_name = 'flatpages/search.html'
    context_object_name = 'info'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


########################################################################################################################

# Создание новой новости.
class NWCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('Posts.add_post',)
    raise_exception = True
    form_class = NWForm
    model = Post
    template_name = 'flatpages/post_edit.html'
    success_url = reverse_lazy("news")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = "NW"
        # Задача сельдерея, которая вызывается.
        send_notification.delay()
        return super().form_valid(form)


class NWEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('Posts.change_post',)
    raise_exception = True
    form_class = NWForm
    model = Post
    template_name = 'flatpages/post_edit.html'
    success_url = reverse_lazy("news")


########################################################################################################################

# Создание новой статьи.
class ATCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('Posts.add_post',)
    raise_exception = True
    form_class = ATForm
    model = Post
    template_name = 'flatpages/post_edit.html'
    success_url = reverse_lazy("article")

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = "AT"
        return super().form_valid(form)


class ATEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('Posts.change_post',)
    raise_exception = True
    form_class = ATForm
    model = Post
    template_name = 'flatpages/post_edit.html'
    success_url = reverse_lazy("article")


########################################################################################################################

# Удаление поста.
class PostDel(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('is_superuser',)
    raise_exception = True
    model = Post
    template_name = 'flatpages/post_del.html'
    success_url = reverse_lazy('allpost')

########################################################################################################################
