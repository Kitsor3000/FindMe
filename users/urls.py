from django.urls import path
from .views import register_view  
from . import views 

urlpatterns = [
    path('register/', register_view, name='register'),
       path('profile/', views.profile_view, name='profile'),
]
