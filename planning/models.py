from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from profiles.models import Profile
from recipe.models import Category, Recipe
from datetime import datetime


class DayCalories(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.PROTECT)
    date = models.DateField()
    calories = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    carbs = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        ordering = ['-date', ]

    def save(self, *args, **kwargs):
        if self.id:
            qs = self.user_recipes.all()
            self.calories = qs.aggregate(value=Sum('calories'))['value'] or 0
            self.fats = qs.aggregate(value=Sum('fats'))['value'] or 0
            self.carbs = qs.aggregate(value=Sum('carbs'))['value'] or 0
            self.protein = qs.aggregate(value=Sum('protein'))['value'] or 0
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("day_calories_detail", kwargs={"pk": self.pk})

    @staticmethod
    def search_query(request):
        qs = DayCalories.objects.filter(profile=request.user.profile)
        start_date = request.GET.get("start_date", datetime.today().date())
        end_date = request.GET.get("end_date", datetime.today().date())
        if end_date > start_date:
            return qs.none()
        qs = qs.filter(date__range=(start_date, end_date))
        return qs


class DayCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    day = models.ForeignKey(DayCalories,  on_delete=models.PROTECT, related_name="day_categories")
    calories = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    carbs = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ['category', 'day']

    def save(self, *args, **kwargs):
        if self.id:
            qs = self.user_category_recipes.all()
            self.calories = qs.aggregate(value=Sum('calories'))['value'] or 0
            self.fats = qs.aggregate(value=Sum('fats'))['value'] or 0
            self.carbs = qs.aggregate(value=Sum('carbs'))['value'] or 0
            self.protein = qs.aggregate(value=Sum('protein'))['value'] or 0
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category.title

    @staticmethod
    def fetch_data_per_category(profile):
        days_list = DayCalories.objects.filter(profile=profile)
        days_list_ids = days_list.values_list("id")
        day_categories = DayCategory.objects.filter(day__id__in=days_list_ids)
        annotated_data = {}
        for category in Category.objects.all():
            qs = day_categories.filter(category=category)
            annotated_data[f"{category.title}"] = {
                "calories": qs.aggregate(total=Sum("calories"))['total'] or 0,
                "protein": qs.aggregate(total=Sum("protein"))['total'] or 0,
                "carbs": qs.aggregate(total=Sum("carbs"))['total'] or 0,
                "fat": qs.aggregate(total = Sum("fats"))['total'] or 0,
            }

        return annotated_data


class UserRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.PROTECT)
    category = models.ForeignKey(DayCategory, on_delete=models.PROTECT, related_name="user_category_recipes")
    day_calories = models.ForeignKey(DayCalories, on_delete=models.PROTECT, related_name='user_recipes')
    qty = models.DecimalField(max_digits=10, decimal_places=2)
    calories = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fats = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    carbs = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        unique_together = ['category', 'recipe']

    def __str__(self):
        return self.recipe.title

    def save(self, *args, **kwargs):
        if self.id:
            qty = self.qty / 100
            self.calories = self.recipe.calories * qty
            self.fats = self.recipe.fats * qty
            self.carbs = self.recipe.carbs * qty
            self.protein = self.recipe.protein * qty
        super().save(*args, **kwargs)
        self.category.save()
        self.day_calories.save()

    def get_edit_url(self):
        return reverse("edit_user_recipe", kwargs={"pk": self.id})

    def get_delete_url(self):
        return reverse("delete_user_recipe", kwargs={"pk": self.id})