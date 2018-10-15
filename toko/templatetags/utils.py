import json as jsonlib
import locale
from django import template
from django.conf import settings
from django.urls import resolve
from django.forms import BoundField
from django.utils.safestring import mark_safe

locale.setlocale(locale.LC_ALL, 'id_ID.utf8')

register = template.Library()

@register.simple_tag
def define(exp):
    return eval(exp)

@register.simple_tag(takes_context=True)
def js(context, src):
    context['scripts'].append(src)
    return ''

@register.simple_tag(takes_context=True)
def jsvar(context, **kwargs):
    context['js_vars'].update(kwargs)
    return ''

@register.simple_tag(takes_context=True)
def if_url(context, name, true_val, false_val=''):
    m = resolve(context['request'].path)
    is_url = m.url_name == name or '%s:%s' % (m.app_name, m.url_name) == name
    return true_val if is_url else false_val

@register.inclusion_tag('toko/pagination/pagination.html')
def pagination(paginator):
    return {'paginator': paginator}

@register.inclusion_tag('toko/errors.html')
def errors(errors):
    return {'errors': errors}

# Filters ===================================================================

@register.filter
def json(val):
    return mark_safe(jsonlib.dumps(val))

@register.filter
def unique(val):
    result = []
    for item in val:
        if not item in result:
            result.append(item)
    return result

@register.filter
def field_error(bound_field):
    if not isinstance(bound_field, BoundField):
        return bound_field
    if bound_field.errors:
        css_class = bound_field.field.widget.attrs.get('class', None)
        if css_class:
            bound_field.field.widget.attrs['class'] = '%s %s' % (css_class, 'is-danger')
        else:
            bound_field.field.widget.attrs['class'] = 'is-danger'
    return bound_field

@register.filter
def money(val):
    return locale.currency(val, grouping=True)