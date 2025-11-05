from django.db import models
from django.contrib.auth.models import User
from missing_persons.models import MissingPerson

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="volunteer_profile")
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    telegram = models.CharField(max_length=100, blank=True)
    viber = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Волонтер: {self.user.username} ({self.region})"


class VolunteerParticipation(models.Model):
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='volunteer_participations')
    person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='search_participants')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('volunteer', 'person')

    def __str__(self):
        return f"{self.volunteer.username} ➜ {self.person.full_name}"
