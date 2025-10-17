from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name = 'users'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path("admin_dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("staff_dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
]
