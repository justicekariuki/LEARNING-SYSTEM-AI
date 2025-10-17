from django.db import models
from django.conf import settings
from students.models import Course

# Create your models here.
class StaffProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile"
    )
    staff_id = models.CharField(max_length=30, unique=True)
    staff_name = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', default='profile_pics/default.jpg'
    )
    courses = models.ManyToManyField(Course, blank=True, related_name='staff_members')  
    def __str__(self):
        return f"{self.user.username} - {self.position}"