from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt import views as jwt_views
from frontend.api.views import homepage_api_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/profile/', include('profiles.api.urls')),
    path("api/", homepage_api_view),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/recipes/', include('recipe.api.urls')),
    path('api/planning/', include('planning.api.urls')),
]