from django.db import models
from django.db.models import Q
from recipe.utils.extras import translate_to_english
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.title

class Recipe(models.Model):
    title = models.CharField(max_length=250, unique=True)
    calories = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    carbs = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.title

    @staticmethod
    def search_recipes(request):
        q = request.GET.get('q')
        translated_q = translate_to_english(q)
        qs = Recipe.objects.filter(Q(title__icontains=translated_q) |
                                   Q(title__startswith=translated_q)
                                   ).distinct()

        return qs