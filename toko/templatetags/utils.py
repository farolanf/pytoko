import json as jsonlib
import locale
from django import template
from django.conf import settings
from django.urls import resolve
from django.forms import BoundField
from django.utils.safestring import mark_safe
from toko.renderers import FormRenderer

locale.setlocale(locale.LC_ALL, 'id_ID.utf8')

register = template.Library()

def init_global(context, name, default):
    context.render_context[name] = context.render_context.get(name, default)

def get_global(context, name, default):
    init_global(context, name, default)
    return context.render_context[name]

@register.simple_tag
def define(exp):
    return eval(exp)

@register.simple_tag(takes_context=True)
def js(context, src):
    get_global(context, 'scripts', []).append(src)
    return ''

@register.simple_tag(takes_context=True)
def css(context, href):
    get_global(context, 'styles', []).append(href)
    return ''

@register.simple_tag(takes_context=True)
def jsvar(context, **kwargs):
    get_global(context, 'js_vars', {}).update(kwargs)
    return ''

@register.simple_tag(takes_context=True)
def scripts(context):
    return get_global(context, 'scripts', [])

@register.simple_tag(takes_context=True)
def styles(context):
    return get_global(context, 'styles', [])

@register.simple_tag(takes_context=True)
def js_vars(context):
    return get_global(context, 'js_vars', {})

@register.simple_tag(takes_context=True)
def if_url(context, name, true_val, false_val=''):
    m = resolve(context['request'].path)
    is_url = m.url_name == name or '%s:%s' % (m.app_name, m.url_name) == name
    return true_val if is_url else false_val

@register.simple_tag
def render_form(serializer, template_pack=None, form=None):
    style = {'template_pack': template_pack} if template_pack else {}
    renderer = FormRenderer(form=form)
    return renderer.render(serializer.data, None, {'style': style})

@register.simple_tag
def render_field(field, style):
    renderer = style.get('renderer', FormRenderer())
    return renderer.render_field(field, style)

@register.simple_tag
def render_widget(field, style):
    renderer = style.get('renderer', FormRenderer())
    return renderer.render_widget(field, style)

@register.inclusion_tag('toko/pagination/pagination.html')
def pagination(paginator):
    return {'paginator': paginator}

@register.inclusion_tag('toko/errors.html')
def errors(errors):
    return {'errors': errors}

@register.inclusion_tag('toko/form/hidden-input.html')
def hidden(name, value):
    return {'name': name, 'value': value}

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