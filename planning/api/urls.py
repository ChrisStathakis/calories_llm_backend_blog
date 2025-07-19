from django.urls import path

from .views import (
    planning_homepage_view, DayCaloriesListApiView, DayCategoryListApiView, UserRecipeApiView,
    DayCaloriesDetailApiView
    )

app_name = "api_planning"

urlpatterns = [
    path('', planning_homepage_view, name="home"),
    path('day-calories/', DayCaloriesListApiView.as_view(), name="day_calories"),
    path("day-calories/<str:date>/", DayCaloriesDetailApiView.as_view(), name="day_calories_detail"),
    path('day-categories/', DayCategoryListApiView.as_view(), name='day_categories'),
    path('user-recipes/', UserRecipeApiView.as_view(), name="user_recipes")
]