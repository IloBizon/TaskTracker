from django_filters import rest_framework as filters

from tasks.models import Task


class TaskFilter(filters.FilterSet):
    creation_date = filters.DateFromToRangeFilter()
    due_date = filters.DateFromToRangeFilter()

    class Meta:
        model = Task
        fields = ["creation_date", "due_date", "status", "priority", "testing_responsible"]