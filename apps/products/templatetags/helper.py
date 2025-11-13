from django.template import Library


register = Library()


@register.filter
def sub(val1, val2):
    return int(val1) / int(val2)