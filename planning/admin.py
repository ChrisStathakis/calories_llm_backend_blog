from django.contrib import admin
from .models import DayCalories, DayCategory, UserRecipe

@admin.register(DayCalories)
class DayCaloriesAdmin(admin.ModelAdmin):
    list_display = ['date', "profile", "calories", "protein", "carbs", "fats"]
    list_filter = ['profile']
    date_hierarchy = "date"

@admin.register(DayCategory)
class DayCategoryAdmin(admin.ModelAdmin):
    list_display = ['day', "category", "calories", "protein", "carbs", "fats"]
    list_filter = ['category', "day__profile"]
    date_hierarchy = "day__date"

@admin.register(UserRecipe)
class UserRecipeAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'category', 'day_calories', 'qty', 'calories']
    list_filter = ['category__category', "category__day__profile"]
    search_fields = ['recipe__title', ]
    date_hierarchy = "category__day__date"