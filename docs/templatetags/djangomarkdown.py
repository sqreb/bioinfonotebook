# -*- coding: utf-8 -*-
from django import template
from django.utils.encoding import force_bytes
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter
import markdown2

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def djangomarkdown(value):
    return mark_safe(markdown2.markdown(force_bytes(value), extras=["code-friendly"]))
