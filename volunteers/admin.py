from django.contrib import admin
from .models import Volunteer, VolunteerParticipation

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('user', 'region', 'city', 'phone_number', 'created_at')
    list_filter = ('region',)
    search_fields = ('user__username', 'region', 'city')

@admin.register(VolunteerParticipation)
class VolunteerParticipationAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'person', 'joined_at')
    search_fields = ('volunteer__username', 'person__full_name')
