from django import template

register = template.Library()


@register.filter
def formated_date(value):
    return value.strftime("%d %b %Y, %H:%M")
