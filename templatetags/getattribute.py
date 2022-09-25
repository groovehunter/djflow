from django import template

register = template.Library()

@register.simple_tag
def getattribute(obj, attr):
    return getattr(obj, attr)

