from django import forms
from .models import Assignment, Feedback

class AssignmentData(forms.Form):
	class meta:
		model = Assignment
		fields = '__all__'

class FeedbackData(forms.Form):
	class meta:
		model = Feedback
		fields = '__all__'