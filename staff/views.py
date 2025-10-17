from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.forms import modelformset_factory
from django import forms
from django.contrib import messages
from students.models import Assignment, Submission, Course, Question
from .models import StaffProfile
from .forms import StaffProfileForm, AssignmentForm, GradeSubmissionForm, QuestionForm, QuizForm
from users.views import is_staff




@login_required
def create_profile(request):
	if hasattr(request.user, 'staff_profile'):
		return redirect('staff:view_profile')  # Prevent duplicate profile
	if request.method == 'POST':
		form = StaffProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			profile.save()
			return redirect('staff:view_profile')
	else:
		form = StaffProfileForm()
	return render(request, 'staff/create_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile = get_object_or_404(StaffProfile, user=request.user)
    return render(request, 'staff/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(StaffProfile, user=request.user)
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('staff:view_profile')
    else:
        form = StaffProfileForm(instance=profile)
    return render(request, 'staff/edit_profile.html', {'form': form})


@login_required
@user_passes_test(is_staff)
def choose_assignment_type(request):
    if request.method == "POST":
        assignment_type = request.POST.get("assignment_type")
        if assignment_type == "FILE":
            return redirect('staff:create_assignment')  # File upload assignment creation view
        elif assignment_type == "QUIZ":
            return redirect('staff:create_quiz')  # Quiz assignment creation view (same form, but user will select type)
    return render(request, "staff/choose_assignment_type.html")



@login_required
@user_passes_test(is_staff)
def create_assignment(request):
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('staff:view_assigned_courses')
    else:
        form = AssignmentForm()
    return render(request, 'staff/create_assignment.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def view_submissions(request):
    # Get assignments created by this staff member
    assignments = Assignment.objects.filter(created_by=request.user)
    # Get submissions for those assignments
    submissions = Submission.objects.filter(assignment__in=assignments).select_related('assignment', 'student')
    return render(request, 'staff/view_submissions.html', {'submissions': submissions})


@login_required
@user_passes_test(is_staff)
def grade_submission(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id, assignment__created_by=request.user)
    if request.method == 'POST':
        form = GradeSubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Submission graded successfully!")
            return redirect('staff:view_submissions')
    else:
        form = GradeSubmissionForm(instance=submission)
    return render(request, 'staff/grade_submission.html', {'form': form, 'submission': submission})

@login_required
@user_passes_test(is_staff)
def view_assigned_courses(request):
    staff_profile = StaffProfile.objects.get(user=request.user)
    courses = staff_profile.courses.all()
    print(courses)  # Debugging line to check courses
    return render(request, 'staff/view_assigned_courses.html', {'courses': courses})


#VIEWS FOR INTERACTIVE QUIZ ASSIGNMENTS
@login_required
@user_passes_test(is_staff)
def create_quiz(request):
    if request.method == "POST":
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.assignment_type = "QUIZ"
            quiz.created_by = request.user
            quiz.save()
            return redirect('staff:add_questions', assignment_id=quiz.id)
    else:
        form = QuizForm()
    return render(request, "staff/create_quiz.html", {"form": form})


@login_required
@user_passes_test(is_staff)
def add_questions(request, assignment_id):
    assignment= get_object_or_404(Assignment, id=assignment_id, assignment_type="QUIZ", created_by=request.user)
    form = QuestionForm(request.POST)
    if form.is_valid():
        question = form.save(commit=False)
        question.assignment = assignment
        question.save()
        return redirect('staff:add_questions', assignment_id=assignment.id)
    else:
        form = QuestionForm()
    return render(request, "staff/add_questions.html", {"form": form, "assignment": assignment})
    

#ADDITIONAL VIEWS FOR LISTING QUIZZES AND ADDING QUESTIONS TO EXISTING QUIZZES
@login_required
@user_passes_test(is_staff)
def list_quizzes(request):
    quizzes = Assignment.objects.filter(created_by=request.user, assignment_type="QUIZ")
    if request.method == "POST":
        quiz_id = request.POST.get("quiz_id")
        quiz = get_object_or_404(Assignment, id=quiz_id, created_by=request.user)
        quiz.delete()
        return redirect("staff:list_quizzes")

    return render(request, "staff/list_quizzes.html", {"quizzes": quizzes})

@login_required
@user_passes_test(is_staff)
def add_questions_to_quiz(request, quiz_id):
    quiz = get_object_or_404(Assignment, id=quiz_id, assignment_type="QUIZ")
    QuestionFormSet = modelformset_factory(Question, form=QuestionForm, extra=1, can_delete=True)

    if request.method == "POST":
        formset = QuestionFormSet(request.POST, queryset=Question.objects.filter(assignment=quiz))
        if formset.is_valid():
            questions = formset.save(commit=False)
            for question in questions:
                question.assignment = quiz
                question.save()
            return redirect("staff:list_quizzes")
    else:
        formset = QuestionFormSet(queryset=Question.objects.filter(assignment=quiz))

    return render(request, "staff/add_questions_to_quiz.html", {"quiz": quiz, "formset": formset})