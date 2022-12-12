import django_filters

from .models import *

class LabFilter(django_filters.FilterSet):
    class Meta:
        model = Lab_Manual
        fields = ['lab_name',
        'instructor',
        'course',
        'activity_name',
        ]
