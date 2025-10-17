from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Staff', 'Staff'),
        ('Admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES)


    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']