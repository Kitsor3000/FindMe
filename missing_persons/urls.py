from rest_framework import routers
from .views import MissingPersonViewSet

from django.urls import path
from . import views as mp_views

router = routers.DefaultRouter()
router.register(r'missing', MissingPersonViewSet)
urlpatterns = [
     path('api/missing-persons/', mp_views.api_missing_persons_list, name='api_missing_persons_list'),
]


urlpatterns += router.urls