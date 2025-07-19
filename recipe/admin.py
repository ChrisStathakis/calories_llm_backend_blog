from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Category, Recipe
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Recipe)
class RecipeAdmin(ImportExportModelAdmin):
    list_display = ['title', 'calories', 'protein', 'carbs', 'fats']
    search_fields = ['title', ]