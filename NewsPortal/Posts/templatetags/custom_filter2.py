from django import template

register = template.Library()


@register.filter()
def post_time(date):
    return date.strftime("%d/%m/%Y")
