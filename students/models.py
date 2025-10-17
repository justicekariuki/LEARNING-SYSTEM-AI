# Create your models here.
from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    admission_number = models.CharField(max_length=30, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    course = models.CharField(max_length=100, blank=True)
    year_of_study = models.IntegerField(default=1)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/', default='profile_pics/default.jpg'
    )

    def __str__(self):
        return f"{self.user.username} - {self.admission_number}"
    
#COURSE ENROLLMENT
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,   # links to your CustomUser
        on_delete=models.SET_NULL,
        null=True, blank=True) # only staff can be chosen

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')  # avoid duplicates

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.code}"


class Grade(models.Model):
    enrollment = models.ForeignKey('Enrollment', on_delete=models.CASCADE, related_name='grades')
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)  # e.g. 89.50
    grade = models.CharField(max_length=2)  # e.g. A, B, C
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.course.code} : {self.grade}"

#ASSIGNMENT AND SUBMISSION MODELS
class Assignment(models.Model):
    ASSIGNMENT_TYPES =[
        ("FILE", "File Upload"),
        ("QUIZ", "Interactive Quiz"),#NEW
    ]
    course = models.ForeignKey("students.Course", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    assignment_type = models.CharField(max_length=10, choices=ASSIGNMENT_TYPES, default="FILE")#NEW
    file = models.FileField(upload_to='assignments/', null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        
    )

    def __str__(self):
        return f"{self.title} - {self.course.name}"


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                limit_choices_to={'user_type': 'student'})
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.assignment.title} by {self.student.username}"

#QUESTION BANK MODELS
class Question(models.Model):
    QUESTION_TYPES = [
        ("MCQ", "Multiple Choice"),
        ("TEXT", "Short Answer"),
    ]
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    # For MCQs
    option_a = models.CharField(max_length=255, blank=True, null=True)
    option_b = models.CharField(max_length=255, blank=True, null=True)
    option_c = models.CharField(max_length=255, blank=True, null=True)
    option_d = models.CharField(max_length=255, blank=True, null=True)
    correct_answer = models.CharField(max_length=255, blank=True, null=True)
    answer_text = models.TextField(blank=True, null=True)  # For TEXT questions



class StudentResponse(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField(null=True, blank=True)   # for text questions
    selected_choice = models.CharField(max_length=1, null=True, blank=True)  # for MCQ
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.student.username} for Question {self.question.id}"
 



