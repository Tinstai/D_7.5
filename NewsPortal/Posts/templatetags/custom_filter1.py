from django import template

register = template.Library()


@register.filter()
def length(words):
    return f"{len(words)}"
