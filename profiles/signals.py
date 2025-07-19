from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from datetime import date

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # create a profile object for the user when the user is created
    if created:
        Profile.objects.create(user=instance,
                               year_of_birth=date.today(),
                               gender="M",
                               activity_lvl=1.55,
                               height=0,
                               weight=0,
                               age=0

                            )