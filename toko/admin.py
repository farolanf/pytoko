from django import forms
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import User, Taxonomy, ProductType, Product, Value, Field, FieldValue, Ad

class FieldForm(forms.ModelForm):

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        if instance:
            self.fields['choices'].queryset = Value.objects.filter(group=instance.group)

class FieldAdmin(admin.ModelAdmin):
    form = FieldForm

class FieldValueForm(forms.ModelForm):

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        if instance:
            self.fields['value'].queryset = instance.field.choices.order_by('-value')

class FieldValueAdmin(admin.ModelAdmin):
    form = FieldValueForm

admin.site.register(User)
admin.site.register(Taxonomy, DraggableMPTTAdmin)

admin.site.register(Value)
admin.site.register(ProductType)
admin.site.register(Product)
admin.site.register(Ad)

admin.site.register(Field, FieldAdmin)
admin.site.register(FieldValue, FieldValueAdmin)


# TODO: bulk add taxonomies from text, see laravel relevant code