from django.dispatch import receiver
from django.db.models.signals import pre_delete
from .models import AdImage

@receiver(pre_delete, sender=AdImage, dispatch_uid='delete_image_file')
def delete_image(sender, instance, **kwargs):
    instance.image.delete()
