from django.db import models
from django.contrib.auth.models import User
from missing_persons.models import MissingPerson

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    missing_person = models.ForeignKey(MissingPerson, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Коментар від {self.user.username}"
