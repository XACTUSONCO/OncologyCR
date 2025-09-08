from django.forms import ModelForm, DateInput, Select
from .models import Patient, Leave
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from user.models import Contact
import math, calendar
from django.db.models import Value, Sum, FloatField, Case, When, Q
from django.db.models.functions import Coalesce

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

        if not from_date or not user:
            return cleaned_data

        # 기본 날짜 검증 (당일 금지, 3개월 이내 제한)
        min_date = today + timedelta(days=1)
        max_month = (today.month + 2 - 1) % 12 + 1
        max_year = today.year + ((today.month + 2 - 1) // 12)
        last_day = date(max_year, max_month + 1, 1) - timedelta(days=1)

        if from_date == today:
            raise ValidationError({'from_date': '당일 휴가 신청은 불가합니다.'})
        if from_date < min_date or from_date > last_day:
            raise ValidationError({'from_date': f'휴가는 {min_date:%Y-%m-%d}부터 {last_day:%Y-%m-%d}까지 신청 가능합니다.'})

        # 이월 휴가 검증
        if kind in ['carry_over', 'carry_over_Half']:
            if from_date.month >= 4 and from_date.month <= 12:
                raise ValidationError({'kind': '이월 휴가는 3월까지 사용 가능합니다.'})
            if from_date.year > today.year:
                raise ValidationError({'kind': '이월 휴가는 당해 연도에만 사용하실 수 있습니다.'})

        # 유저 정보 확인
        try:
            contact = Contact.objects.select_related('team').get(user=user, onco_A=True)
        except Contact.DoesNotExist:
            return cleaned_data  # 재직자가 아니면 제한 없음

        team = contact.team
        if team and team.name in ['GSI', 'CLUE']:
            # 팀 제한 (반차·공가 제외)
            half_day_kinds = ['afternoon_Half', 'morning_Half', 'carry_over', 'carry_over_Half', 'official']
            if kind not in half_day_kinds:
                total_team_members = Contact.objects.filter(team=team, onco_A=True).exclude(team__id=3).count()
                leave_count = Leave.objects.filter(
                    is_deleted=False,
                    from_date=from_date,
                    user__contact__onco_A=True,
                    user__contact__team=team
                ).exclude(Q(kind__in=half_day_kinds) | Q(user__contact__team__id=3)).count()

                if total_team_members > 0 and leave_count >= math.ceil(total_team_members * 0.5):
                    raise ValidationError({'from_date': f"{team.name} 팀은 이미 50% 인원이 휴가 신청하여 제한됩니다."})

        # 근속기간
        years, months = contact.get_career_duration()
        if years == 0 and months == 0:
            raise ValidationError({'from_date': '1개월 만근에 휴가 1일이 발생하므로 사용 불가합니다.'})

        # 월 최대 4일 제한
        target_month_start = date(from_date.year, from_date.month, 1)
        target_month_end = date(from_date.year, from_date.month,calendar.monthrange(from_date.year, from_date.month)[1])

        month_count = Leave.objects.filter(
            user=user,
            is_deleted=False,
            from_date__range=(target_month_start, target_month_end)
        ).aggregate(total=Coalesce(Sum(
            Case(
                When(kind='Monthly', then=Value(1.0)),
                When(kind='Annual', then=Value(1.0)),
                When(kind='morning_Half', then=Value(0.5)),
                When(kind='afternoon_Half', then=Value(0.5)),
                default=Value(0.0),
                output_field=FloatField()
            )
        ), 0.0))['total']

        if kind in ['Annual', 'Monthly', 'morning_Half', 'afternoon_Half']:
            add_value = 1.0 if kind in ['Annual', 'Monthly'] else 0.5
        if month_count + add_value > 4.0:
            raise ValidationError({'from_date': f"{from_date.year}년 {from_date.month}월은 한 달 최대 4일까지만 신청 가능합니다."})

        # 연간 총 사용일수 제한
        fixed_annual = contact.get_fixed_annual()
        fixed_monthly = contact.get_fixed_monthly()
        total_available = fixed_annual + fixed_monthly

        usage_count = Leave.objects.filter(
            user=user,
            is_deleted=False,
            from_date__year=today.year
        ).aggregate(total=Coalesce(Sum(
            Case(
                When(kind='Monthly', then=1.0),
                When(kind='Annual', then=1.0),
                When(kind='morning_Half', then=0.5),
                When(kind='afternoon_Half', then=0.5),
                default=Value(0.0),
                output_field=FloatField()
            )
        ), 0.0))['total']

        if usage_count + add_value > total_available:
            raise ValidationError({
                'from_date': f"사용 가능한 휴가 일수({total_available}일)를 초과할 수 없습니다. "
                             f"(현재 사용: {usage_count}일, 추가 신청: {add_value}일)"
            })

        return cleaned_data
