from django.db import models
from django.contrib.auth.models import User

class MissingPerson(models.Model):
    STATUS_CHOICES = [
       ('missing', 'У розшуку'),
        ('found', 'Знайдено'),
    ]

    CATEGORY_CHOICES = [
    ('child', 'Дитина'),
    ('adult', 'Дорослий'),
    ('elderly', 'Літня людина'),
    ('military', 'Військовий'),
    ('disabled', 'Людина з інвалідністю'),
    ('other', 'Інше'),
]


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    birth_date = models.DateField(null=True, blank=True)
    missing_date = models.DateField()
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='missing_persons/', blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='missing')

    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField("Останнє місце, де бачили", max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)


    def __str__(self):
        return f"{self.full_name} ({self.region})"
