from django import template

register = template.Library()

@register.filter(name='addClass')
def addClass(value, arg):
    return value.as_widget(attrs={'class':arg})

@register.filter(name='getRange')
def getRange(value):
    return range(value)