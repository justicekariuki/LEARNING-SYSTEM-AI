from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from users.models import Profile

class Command(BaseCommand):
    help = "Create default groups and permissions"

    def handle(self, *args, **kwargs):
        # Admin group
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        admin_perms = Permission.objects.filter(codename__in=["can_manage_users", "can_view_dashboard"])
        admin_group.permissions.set(admin_perms)

        # Staff group
        staff_group, _ = Group.objects.get_or_create(name="Staff")
        staff_perms = Permission.objects.filter(codename__in=["can_view_dashboard"])
        staff_group.permissions.set(staff_perms)

        # Student group
        student_group, _ = Group.objects.get_or_create(name="Student")
        student_group.permissions.clear()  # maybe no special perms

        self.stdout.write(self.style.SUCCESS("Roles created successfully"))
