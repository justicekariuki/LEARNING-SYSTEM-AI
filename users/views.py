from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout
from.forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group

#set user-passes-decorator
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_staff(user):
    return user.groups.filter(name='Staff').exists()

def is_student(user):
    return user.groups.filter(name='Student').exists()

# Create your views here.
def home(request):
    return render(request, 'users/base.html')

def signup(request):
    form= UserRegisterForm()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()  # Creates the user
            role = form.cleaned_data.get('role')
            # Assign default role (e.g., Student)
        if role == "Student":
            group = Group.objects.get(name="Student")
        elif role =="Staff":
            group = Group.objects.get(name="Staff")
        elif role == "Admin":
            group = Group.objects.get(name="Admin")
        else:
            group = None

        if group:
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully!')
            return redirect('login')
            # Handle the signup logic here
            pass
    return render(request, 'users/signup.html', {'form': form})

def login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            # Role-based redirects
            if user.groups.filter(name="Admin").exists():
                return redirect("users:admin_dashboard")
            elif user.groups.filter(name="Staff").exists():
                return redirect("users:staff_dashboard")
            elif user.groups.filter(name="Student").exists():
                return redirect("users:student_dashboard")
            else:
                return redirect('users:login')
        messages.error(request, "Invalid username or password")

    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('users:login')
    #return render(request, 'users/logout.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'users/admin_dashboard.html')

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    return render(request, 'users/staff_dashboard.html')

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    return render(request, 'users/student_dashboard.html') 
