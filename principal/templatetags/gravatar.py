from libgravatar import Gravatar
from django import template

register = template.Library()

@register.filter
def gravatar_url(email, size=100):
    return Gravatar(email).get_image(size=size)
