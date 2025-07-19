from rest_framework import serializers

from ..models import DayCategory, DayCalories, UserRecipe

class DayCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = DayCategory
        fields = ['category', 'day', 'calories', 'fats', 'carbs', 'protein']

class DayCaloriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = DayCalories
        fields = ['profile', 'date', 'calories', 'fats', 'carbs', 'protein', 'id']

class UserRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRecipe
        fields = [
            'recipe',
            'category',
            'day_calories',
            'qty',
            'calories',
            'fats',
            'carbs',
            'protein',
    ]