from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from logi_go_app.models.users import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creates a Profile instance whenever a new User instance is created.
    """
    if created:
        Profile.objects.create(user=instance)