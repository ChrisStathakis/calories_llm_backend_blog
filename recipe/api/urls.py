from django.urls import path
from . import views

app_name = "api_recipes"

urlpatterns = [
    path('', views.api_recipe_homepage, name='homepage'),
    path('detail/<int:pk>/', views.RetrieveRecipeApiView.as_view(), name="detail"),
    path('list/', views.RecipeList.as_view(), name='recipe-list'),
    path('create/', views.RecipeCreate.as_view(), name='recipe-create'),
    path('update/<int:pk>/', views.RetrieveUpdateRecipe.as_view(), name='recipe-detail'),
    path("suggest-food/", views.suggest_food_api_view, name="suggest_food"),
    path("analyse-sentence/", views.analyse_sentence_api_view, name="analyse_sentence")
]