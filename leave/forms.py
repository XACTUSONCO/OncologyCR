from django.forms import ModelForm, DateInput, Select
from .models import Patient, Leave
from datetime import date
from django.core.exceptions import ValidationError

class PatientForm(ModelForm):
  class Meta:
    model = Patient
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'from_date': DateInput(attrs={'type': 'datetime', 'class': 'datepicker', 'autocomplete': 'off'}, format='%Y-%m-%d'),
      'end_date': DateInput(attrs={'type': 'datetime', 'class': 'datepicker', 'autocomplete': 'off'}, format='%Y-%m-%d'),
      'user': Select(attrs={"disabled": 'disabled'}),
    }
    fields = ['title', 'from_date', 'end_date', 'memo', 'user']

  def __init__(self, request, *args, **kwargs):
    super(PatientForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['from_date'].input_formats = ('%Y-%m-%d',)
    self.fields['end_date'].input_formats = ('%Y-%m-%d',)
    self.fields['user'].empty_label = request.user.username
    self.initial['from_date'] = request.GET.get('from_date')
    self.fields['from_date'].required = True

class LeaveForm(ModelForm):
    class Meta:
        model = Leave
        widgets = {
            'from_date': DateInput(attrs={'type': 'datetime', 'class': 'datepicker', 'autocomplete': 'off'}, format='%Y-%m-%d'),
            'user': Select(attrs={"disabled": 'disabled'}),
        }
        fields = ['name', 'kind', 'from_date', 'memo', 'user']

    def __init__(self, request, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].input_formats = ('%Y-%m-%d',)
        self.initial['from_date'] = request.GET.get('from_date')
        self.fields['user'].empty_label = request.user.username
        self.initial['name'] = request.user.first_name
        self.fields['from_date'].required = True
        self.fields['kind'].required = True

    def clean(self):
        cleaned_data = super().clean()
        from_date = self.cleaned_data.get('from_date')
        kind = cleaned_data.get('kind')
        today = date.today()

        if kind == 'carry_over' or kind == 'carry_over_Half':
            if from_date.month >= 4 and from_date.month <= 12:
                raise ValidationError({'kind': '이월 휴가는 3월까지 사용 가능합니다.'})
            elif from_date.year > today.year:
                raise ValidationError({'kind': '이월 휴가는 당해 연도에만 사용하실 수 있습니다.'})

        return cleaned_data
