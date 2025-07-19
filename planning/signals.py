from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import UserRecipe

@receiver(post_save, sender=UserRecipe)
def handle_create_data(sender, instance, created, **kwargs):
    if created:
        instance.save()

@receiver(post_delete, sender=UserRecipe)
def handle_user_recipe_delete(sender, instance, **kwargs):
    instance.category.save()
    instance.day_calories.save()