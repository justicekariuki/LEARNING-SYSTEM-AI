# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    class Meta:
        permissions = [
            ("can_view_dashboard", "Can View Dashboard"),
            ("can_manage_users", "Can Manage Users"),
        ]

    def __str__(self):
        return f"{self.user.username} Profile"
