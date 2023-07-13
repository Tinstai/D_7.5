from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Exists
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .models import Subscriber
from Posts.models import Category


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(user=request.user, category=category, ).delete()

    categories_with_subscriptions = Category.objects.annotate(user_subscribed=Exists(
        Subscriber.objects.filter(
            user=request.user,
            category=OuterRef('pk'), ))).order_by("name_category")

    return render(request, 'flatpages/subscriptions.html', {'categories': categories_with_subscriptions}, )
