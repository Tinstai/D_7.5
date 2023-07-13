from django import template

register = template.Library()

censor_words = ["артишок", "баклажан", "брокколи", "батат"]


@register.filter()
def censor(value):
    finder = value.split()
    for _ in finder:
        if isinstance(_, str):
            if _.lower().replace(".", "").replace(",", "").replace(";", "").replace(":", "") in censor_words:
                finder[finder.index(_)] = (_[0] + len(_[1:]) * "*")
            else:
                continue
        else:
            continue
    return " ".join(finder)
