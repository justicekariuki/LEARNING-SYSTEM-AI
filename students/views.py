# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import StudentProfileForm, EnrollmentForm, SubmissionForm
from .models import StudentProfile, Enrollment, Course, Grade, Assignment, Submission, StudentResponse, Question
from users.views import is_student  # Add this import from users app

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    return render(request, 'users/student_dashboard.html') 


@login_required
def create_profile(request):
    if hasattr(request.user, 'student_profile'):
        return redirect('students:view_profile')  # Prevent duplicate profile

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('students:view_profile')
    else:
        form = StudentProfileForm()
    return render(request, 'students/create_profile.html', {'form': form})

@login_required
def view_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    return render(request, 'students/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('students:view_profile')
    else:
        form = StudentProfileForm(instance=profile)
    return render(request, 'students/edit_profile.html', {'form': form})


@login_required
@user_passes_test(is_student)
def enroll_course(request):
    courses = Course.objects.all()
    if request.method == "POST":
        course_ids = request.POST.getlist('courses')
        for course_id in course_ids:
            course = Course.objects.get(id=course_id)
            Enrollment.objects.get_or_create(student=request.user, course=course)
        return redirect("students:my_courses")
    return render(request, "students/enroll_course.html", {"courses": courses})
        
@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    return render(request, 'students/my_courses.html', {'enrollments': enrollments})

@login_required
@user_passes_test(is_student)
def view_grades(request):
    grades = Grade.objects.filter(enrollment__student=request.user)
    return render(request, "students/view_grades.html", {"grades": grades})

#ASSIGNMENTS AND SUBMISSION VIEWS
# View all assignments for enrolled courses
@login_required
@user_passes_test(is_student)
def my_assignments(request): 
    # fetch enrollments for the student
    enrollments = Enrollment.objects.filter(student=request.user)
    # fetch courses the student is enrolled in
    enrolled_courses = [enrollment.course for enrollment in enrollments]
    # fetch assignments for those courses
    assignments = Assignment.objects.all()
    #assignments = Assignment.objects.filter(course__in=enrolled_courses)
    return render(request, "students/my_assignments.html", {"assignments": assignments})


# View a single assignment (details)
@login_required
@user_passes_test(is_student)
def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    questions = assignment.questions.all()  # Fetch all questions linked to the assignment
    return render(request, "students/assignment_detail.html", {"assignment": assignment, "questions": questions})

 #Submit an assignment
@login_required
@user_passes_test(is_student)
def submit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == "POST":
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            return redirect("students:my_assignments")
    else:
        form = SubmissionForm()

    return render(request, "students/submit_assignment.html", {"form": form, "assignment": assignment})


# View my submissions (with grades if available)
@login_required
@user_passes_test(is_student)
def my_submissions(request):
    submissions = Submission.objects.filter(student=request.user)
    return render(request, "students/my_submissions.html", {"submissions": submissions})

#INTERACTIVE ASSESMENT ENGINE VIEWS
@login_required
@user_passes_test(is_student)
def take_quiz(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, assignment_type="QUIZ")
    questions = assignment.questions.all()
    # Debugging: Print questions to the console
    print(f"Questions for assignment {assignment_id}: {questions}")

    if request.method == "POST":
        #score = 0
        #total = questions.count()
        # Process each question's answer
        for question in questions:
            user_answer = request.POST.get(f"question_{question.id}")
            if question.question_type == "MCQ":
                #SAVE SELECTED CHOICE
                user_answer = user_answer.upper() if user_answer else None
                StudentResponse.objects.create(
                    student=request.user,
                    question=question,
                    selected_choice=user_answer
                )
                #if user_answer == question.correct_answer:
                    #score += 1

            elif question.question_type == "TEXT":
                    StudentResponse.objects.create(
                        student=request.user,
                        question=question,
                        answer_text=user_answer
                    )
        return redirect('students:quiz_result', assignment_id=assignment.id)
    return render(request, "students/take_quiz.html", {"assignment": assignment, "questions": questions})

@login_required
@user_passes_test(is_student)
def quiz_result(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id, assignment_type="QUIZ")
    questions = assignment.questions.all()
    responses = StudentResponse.objects.filter(student=request.user, question__in=questions)
    score = 0
    total = questions.count()
    for question in questions:
        if question.question_type == "MCQ":
            response = responses.filter(question=question).first()
            if response and response.selected_choice:
                # Compare the selected choice with the correct answer
                if response.selected_choice == question.correct_answer:
                   score += 1
        
        elif question.question_type == "TEXT":
            response = responses.filter(question=question).first()
            if response and response.answer_text:
                # Compare the submitted answer with the correct answer
                if response.answer_text.strip().lower() == question.answer_text.strip().lower():
                    score += 1  # Increment score for correct TEXT answers

    return render(request, "students/quiz_result.html", {
        "assignment": assignment,
        "score": score,
        "total": total,
        "responses": responses,
        "questions": questions,
    })