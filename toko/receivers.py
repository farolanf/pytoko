from django.dispatch import receiver
from django.db.models.signals import pre_delete, m2m_changed
from .models import File, Product, Field

@receiver(pre_delete, sender=File, dispatch_uid='delete_file')
def delete_file(sender, instance, **kwargs):
    instance.file.delete()

@receiver(m2m_changed, sender=Product.specs.through, dispatch_uid='unique_product_spec')
def unique_product_spec(sender, instance, pk_set, action, reverse, model, **kwargs):
    if action == 'pre_add':
        if not reverse:
            fields = Field.objects.filter(values__in=pk_set)
            assert not sender.objects.filter(
                product=instance, 
                fieldvalue__field__in=fields
            ).exists(), 'Duplicate specs'