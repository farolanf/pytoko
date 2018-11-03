from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import File

@receiver(pre_delete, sender=File, dispatch_uid='delete_file')
def delete_file(sender, instance, **kwargs):
    instance.file.delete()