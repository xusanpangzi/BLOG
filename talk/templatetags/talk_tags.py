from ..models import Talk
from django import template

register = template.Library()
@register.simple_tag
def archives1():
    return Talk.objects.dates('created_time','month',order='DESC')