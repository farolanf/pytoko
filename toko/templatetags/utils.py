import os
import re
import json as jsonlib
import locale
from django import template
from django.conf import settings
from django.urls import resolve
from django.forms import BoundField
from django.utils.safestring import mark_safe
from toko.renderers import FormRenderer
from toko.models import Taxonomy

register = template.Library()

def get_attribute(obj, attrs):
    for attr in attrs:
        if hasattr(obj, attr):
            obj = getattr(obj, attr)
        elif hasattr(obj, '__getitem__'):
            try:
                obj = obj.__getitem__(attr)
            except TypeError as exc:
                obj = obj.__getitem__(int(attr))
    return obj

@register.simple_tag
def env(key, default):
    return os.getenv(key, default)

@register.simple_tag
def define(exp):
    return eval(exp)

@register.simple_tag(takes_context=True)
def init_scripts_context(context):
    context['global'] = {
        'scripts': [],
        'styles': [],
        'js_vars': {},
    }
    return ''

@register.simple_tag(takes_context=True)
def js(context, src):
    context['global']['scripts'].append(src)
    return ''

@register.simple_tag(takes_context=True)
def css(context, href):
    context['global']['styles'].append(href)
    return ''

@register.simple_tag(takes_context=True)
def jsvar(context, **kwargs):
    context['global']['js_vars'].update(kwargs)
    return ''

@register.simple_tag(takes_context=True)
def if_url(context, name, true_val, false_val=''):
    m = resolve(context['request'].path)
    is_url = m.url_name == name or '%s:%s' % (m.app_name, m.url_name) == name
    return true_val if is_url else false_val

@register.simple_tag(takes_context=True)
def render_form(context, serializer, template_pack=None, form=None):
    style = {'template_pack': template_pack} if template_pack else {}
    renderer = FormRenderer(form=form)
    return renderer.render(serializer.data, None, {'style': style, 'global': context['global']})

@register.simple_tag(takes_context=True)
def render_field(context, field, style):
    renderer = style.get('renderer', FormRenderer())
    return renderer.render_field(field, style, {'global': context['global']})

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

@register.inclusion_tag('toko/script.html')
def script(path, min=False):
    return {'url': ('%s.min.js' if min else '%s.js') % path}

@register.inclusion_tag('toko/category-menu.html')
def category_menu():
    return {'menu': Taxonomy.objects.get(slug='kategori').get_descendants()}

# Filters ===================================================================

@register.filter
def attr(obj, dotattr):
    attrs = dotattr.split('.')
    return get_attribute(obj, attrs)

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
def money(val, frac=True):
    nstr = locale.currency(val, grouping=True)
    if not frac:
        nstr = nstr[:-3]
    return nstr

@register.filter
def mark(text, keyword):
    
    def repl(match):
        keyword = match.group(0)
        return '<span class="keyword-highlight">%s</span>' % keyword

    text = re.sub(keyword, repl, text, flags=re.IGNORECASE)
    return mark_safe(text)