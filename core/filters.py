import django_filters
from django.db.models import Q

from .models import Post


class PostFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(field_name='written_by__username', lookup_expr='icontains')
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='icontains')
    keyword = django_filters.CharFilter(method='filter_by_keyword', label='Keyword (in title or content)')
    date = django_filters.DateFromToRangeFilter(field_name='created_at')

    class Meta:
        model = Post
        fields = ['author', 'tags', 'date']

    def filter_by_keyword(self, queryset, name, value):
        return queryset.filter(Q(title__icontains=value) | Q(content__icontains=value))
