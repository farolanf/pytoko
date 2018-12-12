from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver
from .models import File, FieldValue

@receiver(pre_delete, sender=File, dispatch_uid='delete_file')
def delete_file(sender, instance, **kwargs):
    instance.file.delete()

@receiver(pre_save, sender=FieldValue, dispatch_uid='group_field_value')
def group_field_value(sender, instance, **kwargs):
    if instance.field.group != instance.value.group:
        raise ValidationError({
            'value': ['Field and value groups must be equal']
        })