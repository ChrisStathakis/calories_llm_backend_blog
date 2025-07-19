from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
import json
from ..models import Recipe
from .serializers import RecipeSerializer
from recipe.utils.llm_service import llm_service


@api_view(['GET'])
def api_recipe_homepage(request, format=None):
    return Response({
        'recipes': reverse('api_recipes:recipe-list', request=request, format=format),
        "suggest_food": reverse("api_recipes:suggest_food", request=request, format=format),
        "analyse_sentence": reverse("api_recipes:analyse_sentence", request=request, format=format)

    })


@api_view(['GET', ])
def suggest_food_api_view(request, format=None):
    q = request.GET.get("q")
    llm_analysis = llm_service.ask_llm(q)
    result_list = []

    return Response({
        "q": q if q else "No data",
        "llm_analysis": llm_analysis,
        "result_list": result_list

    })


@api_view(['GET', ])
def analyse_sentence_api_view(request, format=None):
    q = request.GET.get("q")
    llm_analysis = llm_service.get_nutrition_info(q)
    result_list = {}
    for suggested_food in llm_service.string_to_list(llm_analysis):
        qs = Recipe.objects.filter(title__icontains=suggested_food[0])
        qs_dumped = json.dumps(RecipeSerializer(qs, many=True).data)
        result_list[suggested_food[0]] = {
            "qty": suggested_food[1],
            "title": suggested_food[0],
            "query": qs_dumped  # RecipeSerializer(qs, many=True) if qs.exists() else "No data"
        }
    return Response({
        "sentence": q,
        "llm_analysis": llm_analysis,
        "result_list": result_list
    })


class RecipeList(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeCreate(CreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, ]


class RetrieveRecipeApiView(RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RetrieveUpdateRecipe(RetrieveUpdateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.user == request.user
        return True


class DestroyApiRecipe(DestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, ]