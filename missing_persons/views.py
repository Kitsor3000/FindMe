from django.shortcuts import render

from rest_framework import viewsets, filters
from .models import MissingPerson
from .serializers import MissingPersonSerializer

class MissingPersonViewSet(viewsets.ModelViewSet):
    queryset = MissingPerson.objects.all().order_by('-created_at')
    serializer_class = MissingPersonSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'region', 'city', 'status']

