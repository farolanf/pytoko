from django import forms
from django.contrib import admin
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

    def __init__(self, *args, instance=None, **kwargs):
        super().__init__(*args, instance=instance, **kwargs)
        if instance:
            self.fields['value'].queryset = instance.field.choices.order_by('-value')

class FieldValueAdmin(admin.ModelAdmin):
    form = FieldValueForm
    fields = ('field', 'value')
    list_display = ('field', 'value', 'product')

class FieldValueInline(NestedTabularInline):
    model = FieldValue
    extra = 1

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