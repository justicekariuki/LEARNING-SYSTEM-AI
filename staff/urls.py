from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('profile/create/', views.create_profile, name='create_profile'),
    path('profile/view/', views.view_profile, name='view_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('choose_assignment_type/', views.choose_assignment_type, name='choose_assignment_type'),
    path('create_assignment/', views.create_assignment, name='create_assignment'),
    path('view_submissions/', views.view_submissions, name='view_submissions'),
    path('grade_submission/<int:submission_id>/', views.grade_submission, name='grade_submission'),
    path('assigned-courses/', views.view_assigned_courses, name='view_assigned_courses'),
    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('add_questions/<int:assignment_id>/', views.add_questions, name='add_questions'),
    path("quizzes/", views.list_quizzes, name="list_quizzes"),
    path("quizzes/<int:quiz_id>/add-questions/", views.add_questions_to_quiz, name="add_questions_to_quiz"),

]
