from django.urls import path
from . import views

urlpatterns = [
    path("apply/", views.become_volunteer, name="become_volunteer"),
    path("dashboard/", views.volunteer_dashboard, name="volunteer_dashboard"),
     path('stop/', views.stop_being_volunteer, name='stop_being_volunteer'),
    path("join/<int:person_id>/", views.join_search, name="join_search"),
]
