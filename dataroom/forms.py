from django.forms import ModelForm, DateTimeInput, Select
from .models import training_schedule
from django import forms

class TrainingForm(ModelForm):
  class Meta:
    model = training_schedule
    widgets = {'date': forms.DateTimeInput(format=('%Y-%m-%d %H:%M'), attrs={'autocomplete': 'off', 'type': 'datetime'})}
    fields = ['topic', 'trainer', 'date', 'location', 'memo']

  def __init__(self, request, *args, **kwargs):
    super(TrainingForm, self).__init__(*args, **kwargs)
    self.fields['date'].input_formats = ('%Y-%m-%d %H:%i')
    self.fields['date'].required = True
