from django import forms
from .models import Quiz, Question, QuizAttempt, Attempt


class QuizTakerForm(forms.Form):
    choices = [
        ('A','A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]
    chosen = forms.ChoiceField(choices=choices, required=False, widget=forms.RadioSelect)

