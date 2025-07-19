from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


@api_view(['GET', ])
def homepage_api_view(request, format=None):
    return Response({
        "profiles": reverse("api_profile:home", request=request, format=format),
        "recipes": reverse("api_recipes:homepage", request=request, format=format),
        "planning": reverse("api_planning:home", request=request, format=format),

    })