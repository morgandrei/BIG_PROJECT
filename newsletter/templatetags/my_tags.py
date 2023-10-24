from django import template

register = template.Library()


@register.filter()
def my_media(val):
    if val:
        return f'/media/{val}'
    return '#'


@register.simple_tag
def mediapath(val):
    if val:
        return f'/media/{val}'
    return '#'