from django import forms
from .models import StaffProfile
from students.models import Assignment, Submission, Course, Question

class StaffProfileForm(forms.ModelForm):
	class Meta:
		model = StaffProfile
		fields = ['staff_id', 'staff_name', 'department', 'position', 'bio', 'profile_picture']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["course", "title", "description", "due_date", "file"]
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(instructor=user)


class QuizForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["course", "title", "description", "due_date"]
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['course'].queryset = Course.objects.filter(instructor=user)

class GradeSubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade', 'feedback']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'answer_text']

    def clean(self):
        cleaned_data = super().clean()
        question_type = cleaned_data.get("question_type")

        if question_type == "MCQ":
            if not all([cleaned_data.get("option_a"), cleaned_data.get("option_b")]):
                raise forms.ValidationError("MCQs must have at least two options.")
            if not cleaned_data.get("correct_answer"):
                raise forms.ValidationError("MCQs must have a correct answer.")
        elif question_type == "TEXT":
            if not cleaned_data.get("answer_text"):
                raise forms.ValidationError("Text questions must have an answer text.")

        return cleaned_data


