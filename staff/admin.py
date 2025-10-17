from django.contrib import admin
from .models import StaffProfile

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'position']
    filter_horizontal = ['courses']  # Makes ManyToMany field easier to manage
# If Course is already registered in students/admin.py, do not register it again here

