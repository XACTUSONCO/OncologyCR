from django.forms import ModelForm, DateInput, Select
from .models import Patient, Leave
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from user.models import Contact
from django.db.models import Q
import math

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
        self.request = request  # 저장해두기
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].input_formats = ('%Y-%m-%d',)
        self.initial['from_date'] = request.GET.get('from_date')
        self.fields['user'].empty_label = request.user.username
        self.initial['name'] = request.user.first_name
        self.fields['from_date'].required = True
        self.fields['kind'].required = True

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        kind = cleaned_data.get('kind')
        user = self.request.user
        today = date.today()

        # 기본 날짜 검증 (당일 금지, 3개월 이내 제한)
        min_date = today + timedelta(days=1)
        max_month = (today.month + 2 - 1) % 12 + 1
        max_year = today.year + ((today.month + 2 - 1) // 12)
        last_day = date(max_year, max_month + 1, 1) - timedelta(days=1)

        if kind in ['carry_over', 'carry_over_Half']:
            if not from_date:
                return cleaned_data
            if from_date.month >= 4 and from_date.month <= 12:
                raise ValidationError({'kind': '이월 휴가는 3월까지 사용 가능합니다.'})
            elif from_date.year > today.year:
                raise ValidationError({'kind': '이월 휴가는 당해 연도에만 사용하실 수 있습니다.'})

        if not from_date or not user:
            return cleaned_data

        if from_date < min_date or from_date > last_day:
            raise ValidationError({'from_date': f'휴가는 {min_date.strftime("%Y-%m-%d")}부터 {last_day.strftime("%Y-%m-%d")}까지 신청 가능합니다.'})
        
        # 당일 신청 제한
        if from_date == today:
            raise ValidationError({'from_date': '당일 휴가 신청은 불가합니다.'})

        # 유저 정보 확인
        try:
            contact = Contact.objects.select_related('team').get(user=user, onco_A=True)
        except Contact.DoesNotExist:
            return cleaned_data  # 재직자가 아니면 제한 없음

        team = contact.team
        if not team or team.name not in ['GSI', 'CLUE']:
            return cleaned_data  # 제한 팀 아님

        # 반차/공가 종류는 제한 대상에서 제외
        half_day_kinds = ['afternoon_Half', 'morning_Half', 'carry_over_Half', 'official']
        if kind in half_day_kinds:
            return cleaned_data

        # 팀 전체 인원수 (재직자만, team_id 동일, 제외 팀(id=3) 아님)
        total_team_members = Contact.objects.filter(
            team=team,
            onco_A=True
        ).exclude(team__id=3).count()

        # 해당 날짜에 신청된 인원수 (삭제 안됨, 재직자, 제외 kind/team 아닌 사람들)
        leave_count = Leave.objects.filter(
            is_deleted=False,
            from_date=from_date,
            user__contact__onco_A=True,
            user__contact__team=team
        ).exclude(
            Q(kind__in=half_day_kinds) | Q(user__contact__team__id=3)
        ).count()

        if total_team_members == 0:
            return cleaned_data  # 0으로 나누기 방지

        limit = math.ceil(total_team_members * 0.5)
        if leave_count >= limit:
            raise ValidationError({'from_date': f"{team.name} 팀은 해당 날짜에 이미 50% 인원이 휴가 신청하여 제한됩니다."})

        print("=== CLEAN STARTED ===")
        print("user:", user)
        print("from_date:", from_date)
        print("kind:", kind)
        
        return cleaned_data
