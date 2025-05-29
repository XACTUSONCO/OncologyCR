import django_filters
from .models import Research

class ListFilter(django_filters.FilterSet):
    class Meta:
        model = Research
        fields = ['research_name']
