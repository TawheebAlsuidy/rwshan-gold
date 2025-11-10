from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models.core_models import GeneralSetting


@receiver(post_save, sender=GeneralSetting)
def create_general_setting(sender, instance, created, **kwargs):
    if created:
        print(f"New general setting created: {instance.key}")