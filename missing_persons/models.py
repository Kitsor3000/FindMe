from django.db import models
from django.contrib.auth.models import User

class MissingPerson(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активне'),
        ('found', 'Знайдено'),
        ('archived', 'Архівовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    birth_date = models.DateField(null=True, blank=True)
    missing_date = models.DateField()
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='missing_persons/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.region})"
