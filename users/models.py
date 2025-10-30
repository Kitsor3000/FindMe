from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'Користувач'),
        ('volunteer', 'Волонтер'),
        ('police', 'Поліція'),
        ('admin', 'Адміністратор'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField("Телефон", max_length=20, blank=True)
    role = models.CharField("Роль", max_length=20, choices=ROLE_CHOICES, default='user')
    photo = models.ImageField("Фото профілю", upload_to='users/photos/', blank=True, null=True)
    bio = models.TextField("Про себе", blank=True, null=True)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)
    updated_at = models.DateTimeField("Останнє оновлення", auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()
