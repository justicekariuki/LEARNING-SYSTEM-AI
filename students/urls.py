from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/view/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('enroll/', views.enroll_course, name='enroll_course'),  # New URL for course enrollment
    path('my_courses/', views.my_courses, name='my_courses'),  # New URL for viewing enrolled courses
    path('grades/', views.view_grades, name='view_grades'),  # New URL for viewing grades
    path('assignments/', views.my_assignments, name='my_assignments'),  # New URL for viewing assignments
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),  # New URL for viewing a specific assignment
    path('assignments/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),  # New URL for submitting an assignment
    path('assignments/submissions/', views.my_submissions, name='my_submissions'),  # New URL for viewing submissions
    path('quiz/<int:assignment_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:assignment_id>/result/', views.quiz_result, name='quiz_result'),
]