from rest_framework import routers
from .views import UserViewSet, UserProfileViewSet
from django.urls import path
from .views_auth import register_user


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('register/', register_user, name='register'),  
]

urlpatterns += router.urls