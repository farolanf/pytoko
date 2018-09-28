import os
from django import template

env = os.getenv('ENV')

register = template.Library()

@register.simple_tag
def mix(file):
    # TODO: read mix-manifest to work with versioning
    return file if env == 'production' else 'http://localhost:8080/%s' % file