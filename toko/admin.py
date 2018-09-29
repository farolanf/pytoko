from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import User, Taxonomy

admin.site.register(User)
admin.site.register(Taxonomy, DraggableMPTTAdmin)

# TODO: bulk add taxonomies from text, see laravel relevant code