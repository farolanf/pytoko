from django import forms
from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from nested_inline.admin import NestedModelAdmin, NestedTabularInline
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

    class Media:
        js = ('/static/toko/js/field-value.js',)

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        if instance:
            self.fields['value'].queryset = instance.field.choices.order_by('value')

class FieldValueAdmin(admin.ModelAdmin):
    form = FieldValueForm
    fields = ('field', 'value')
    list_display = ('field', 'value', 'product')

class FieldValueInlineFormSet(BaseInlineFormSet):

    def _construct_form(self, i, **kwargs):
        form = super()._construct_form(i, **kwargs)
        if i < self.instance.specs.all().count():
            field = self.instance.specs.order_by('id').all()[i].field
            form.fields['value'].queryset = field.choices.order_by('value')
        else:
            form.fields['value'].queryset = Field.objects.none()
        return form

class FieldValueInline(NestedTabularInline):
    model = FieldValue
    extra = 1
    formset = FieldValueInlineFormSet

    class Media:
        js = ('/static/toko/js/field-value.js',)

class ProductAdmin(admin.ModelAdmin):
    inlines = (FieldValueInline,)
    readonly_fields = ('ad',)

class ProductInline(NestedTabularInline):
    model = Product
    inlines = (FieldValueInline,)

class AdAdmin(NestedModelAdmin):
    inlines = (ProductInline,)

admin.site.register(User)
admin.site.register(Taxonomy, DraggableMPTTAdmin)

admin.site.register(Value)
admin.site.register(ProductType)
admin.site.register(Product, ProductAdmin)
admin.site.register(Ad, AdAdmin)


admin.site.register(Field, FieldAdmin)
admin.site.register(FieldValue, FieldValueAdmin)