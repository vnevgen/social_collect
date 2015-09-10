__author__ = 'vitaly'


import re
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import urlize as urlize_impl

import datetime

register = template.Library()

@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def urlize_target_blank(value, limit, autoescape=None):
    return mark_safe(urlize_impl(value, trim_url_limit=int(limit), nofollow=True, autoescape=autoescape).replace('<a', '<a target="_blank"'))

@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def urlize_screen_names(value, service="twitter", autoescape=None):


    # TODO: fix issue with email adress
    username_re = re.compile(r'@([A-Za-z0-9_]+)')

    if service == "twitter":
        service_link = "https://twitter.com/"
    elif service == "instagram":
        service_link = "https://instagram.com/"
    else:
        service_link = ""

    html = username_re.sub(lambda m: '<a target="_blank" href="%s%s">%s</a>' % (service_link, m.group(1), m.group(0)), value)
    return html


@register.filter(is_safe=True, needs_autoescape=True)
@stringfilter
def urlize_vk_screen_names(value, autoescape=None):

    vk_re = re.compile(r'\[(^[a-z]*|[a-z][^]]*)]')

    html = vk_re.sub(lambda m: '<a target="_blank" href="https://vk.com/%s">%s</a>' % (m.group(1).split('|')[0], m.group(1).split('|')[1]), value)

    return html


@register.filter
def get_formatted_time(value):
    try:
        return datetime.datetime.fromtimestamp(int(value)).strftime('%a, %d %b %Y %H:%M')
    except AttributeError:
        return ''


@register.filter
def is_empty(value):
    return value == ""

@register.filter
def truncate(value, limit=80):

    if len(value) <= limit:
        return value

    # Cut the string
    value = "%s..." % value[:limit]

    # Join the words and return
    return value


@register.filter
def wrap_counter(value, icon, autoescape=None):

    shadowed = ""

    if value == 0:
        shadowed = "shadowed"

    return mark_safe('<span class="%s"><i class="fa %s"></i> %s</span>' % (shadowed, icon, value))
