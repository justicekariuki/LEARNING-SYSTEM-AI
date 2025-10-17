from django import forms
from .models import StudentProfile, Enrollment, Course, Submission

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['admission_number', 'date_of_birth', 'course', 'year_of_study', 'bio', 'profile_picture']


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']
