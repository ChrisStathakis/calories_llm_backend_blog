from django_filters import rest_framework as filters

from planning.models import DayCalories, DayCategory, UserRecipe

class DateRangeFilter(filters.FilterSet):
    date_start = filters.DateFilter(field_name='date', lookup_expr="gte")
    date_end = filters.DateFilter(field_name="date", lookup_expr="lte")

    class Meta:
        model = DayCalories
        fields = ['date', ]

class DayCategoryFilter(filters.FilterSet):
    date_start = filters.DateFilter(field_name='day', lookup_expr="gte")
    date_end = filters.DateFilter(field_name="day", lookup_expr="lte")

    class Meta:
        model = DayCategory
        fields = ['day', ]