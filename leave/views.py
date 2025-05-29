import datetime, calendar
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q, Value, When, IntegerField, Case, FloatField, Sum, F, ExpressionWrapper, DateField, DurationField, Count
from django.db.models.functions import Coalesce, Cast
from django.contrib.auth.decorators import login_required

from research.models import Research
from user.models import Contact
from feedback.models import Feedback
from .forms import LeaveForm, PatientForm
from .models import Leave, Patient
from dateutil import relativedelta


# Create your views here.
@login_required()
def leave_calendar(request):
    all_events = Leave.objects.filter(is_deleted=False)
    user = request.user
    this_month = datetime.date.today().month
    this_year = datetime.date.today().year

    if Contact.objects.filter(user_id=user.id, onco_A=1):
        today = datetime.date.today()
        # 1년차 미만 - 12월 이전/이후 입사자 구분하기 위함
        december = datetime.date(datetime.date.today().year - 1, 12, 1)
        december_str = datetime.datetime.strftime(december, '%Y-%m-%d')
        # 입사일
        career_date = Contact.objects.filter(user_id=user.id).values_list('career', flat=True)[0]
        years, days_remaining = divmod((today - career_date).days, 365)
        months = days_remaining // 30
        if user.id == 199:  # 류영진 선생님: 연차 1년 추가
            cal_career = (years + 1, months)
        else:
            cal_career = (years, months)  # 단순 튜플로 저장
        
        #cal_career = divmod((today - career_date).days, 365), divmod((today - career_date).days, 365)[1] // 30

        career_str = datetime.datetime.strftime(career_date, '%Y-%m-%d')
        career = datetime.datetime.strptime(career_str, '%Y-%m-%d')

        # 1개월 미만
        if (cal_career[0] == 0 and cal_career[1] == 0):
            fixed_annual = int(0)
        # 1개월 경과시
        elif (cal_career[0] == 0 and cal_career[1] <= 2):
            fixed_annual = int(1)
        # 3개월 경과시
        elif (cal_career[0] == 0 and cal_career[1] <= 5):
            fixed_annual = int(2)
        # 6개월 경과시
        elif (cal_career[0] == 0 and cal_career[1] <= 8):
            fixed_annual = int(3)
        # 9개월 경과시
        elif (cal_career[0] == 0 and cal_career[1] <= 12):
            fixed_annual = int(4)

        # 2년차
        elif cal_career[0] == 1 and cal_career[1] >= 0:
            fixed_annual = int(8)
        # 3년차
        elif cal_career[0] == 2 and cal_career[1] >= 0:
            fixed_annual = int(10)
        # 4년차
        elif cal_career[0] == 3 and cal_career[1] >= 0:
            fixed_annual = int(12)
        # 5년차 이상
        elif cal_career[0] >= 4 and cal_career[1] >= 0:
            fixed_annual = int(13)

        # 1개월 미만  <--- 월차 --->
        if (cal_career[0] == 0 and cal_career[1] == 0):
            fixed_monthly = float(0)
        # 1년차 미만 (12월 이전 입사자)
        elif (cal_career[0] == 0 and cal_career[1] != 0 and career_str < december_str):
            fixed_monthly = today.month
        # 1년차 미만 (12월 이후 입사자)
        elif (cal_career[0] == 0 and cal_career[1] != 0 and career_str >= december_str):
            fixed_monthly = relativedelta.relativedelta(today, career).months
        # 1년차 이상
        elif (cal_career[0] != 0 and (cal_career[1] != 0 or cal_career[1] == 0)):
            fixed_monthly = float(12)

        # 이월 휴가
        # 1년차 미만 - 12월 이전/이후 입사자 구분하기 위함
        december_carry_over = datetime.date(datetime.date.today().year - 2, 12, 1)
        december_carry_over_str = datetime.datetime.strftime(december_carry_over, '%Y-%m-%d')
        last_of_day_year = datetime.date(datetime.date.today().year - 1, 12, 31)  # 기준

        # 작년 12/31 기준 근무기간
        lastYearCareer_years, lastYearCareer_days_remaining = divmod((last_of_day_year - career_date).days, 365)
        lastYearCareer_months = lastYearCareer_days_remaining // 30
        if user.id == 199:  # 류영진 선생님: 연차 1년 추가
            cal_lastYearCareer = (lastYearCareer_years + 1, lastYearCareer_months)  # 단순 튜플로 저장
        else:
            cal_lastYearCareer = (lastYearCareer_years, lastYearCareer_months)  # 단순 튜플로 저장

        #cal_lastYearCareer = divmod((last_of_day_year - career_date).days, 365), \
        #                        divmod((last_of_day_year - career_date).days, 365)[1] // 30

        # 1개월 미만
        if (cal_lastYearCareer[0] == 0 and cal_lastYearCareer[1] == 0):
            lastYearFixedAnnual = int(0)
        elif cal_lastYearCareer[0] < 0:
            lastYearFixedAnnual = int(0)
        # 1개월 경과시
        elif (cal_lastYearCareer[0] == 0 and cal_lastYearCareer[1] <= 2):
            lastYearFixedAnnual = int(1)
        # 3개월 경과시
        elif (cal_lastYearCareer[0] == 0 and cal_lastYearCareer[1] <= 5):
            lastYearFixedAnnual = int(2)
        # 6개월 경과시
        elif (cal_lastYearCareer[0] == 0 and cal_lastYearCareer[1] <= 8):
            lastYearFixedAnnual = int(3)
        # 9개월 경과시
        elif (cal_lastYearCareer[0] == 0 and cal_lastYearCareer[1] <= 12):
            lastYearFixedAnnual = int(4)

        # 2년차
        elif cal_lastYearCareer[0] == 1 and cal_lastYearCareer[1] >= 0:
            lastYearFixedAnnual = int(8)
        # 3년차
        elif cal_lastYearCareer[0] == 2 and cal_lastYearCareer[1] >= 0:
            lastYearFixedAnnual = int(10)
        # 4년차
        elif cal_lastYearCareer[0] == 3 and cal_lastYearCareer[1] >= 0:
            lastYearFixedAnnual = int(12)
        # 5년차 이상
        elif cal_lastYearCareer[0] >= 4 and cal_lastYearCareer[1] >= 0:
            lastYearFixedAnnual = int(13)

        # 1개월 미만  <-- 월차 -->
        if (cal_lastYearCareer[0] == 0 and cal_lastYearCareer[1] == 0):
            lastYearFixedMonthly = float(0)
        # 1년차 미만 (12월 이전 입사자)
        elif (cal_lastYearCareer[0] == 0 and cal_lastYearCareer[1] != 0 and career_str < december_carry_over_str):
            lastYearFixedMonthly = float(12)
        # 1년차 미만 (12월 이후 입사자)
        elif (cal_lastYearCareer[0] == 0 and cal_lastYearCareer[1] != 0 and career_str >= december_carry_over_str):
            lastYearFixedMonthly = relativedelta.relativedelta(last_of_day_year, career).months
        # 1년차 이상
        elif (cal_lastYearCareer[0] != 0 and (cal_lastYearCareer[1] != 0 or cal_lastYearCareer[1] == 0)):
            lastYearFixedMonthly = float(12)

        # 사용 현황 Table - 사용한 일수와 사용 가능한 일수
        # 일 년의 첫 날과 마지막 날
        first_of_year = datetime.date(today.year, 1, 1)
        last_of_year = datetime.date(today.year, 12, 31)
        # 한 달의 첫 날과 마지막 날
        first_day = datetime.date(today.year, today.month, 1)
        #last_day = datetime.date(today.year, today.month+1, 1) - datetime.timedelta(days=1)
        last_day = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        # 등록한 휴가가 없을 경우 (ex: 신규가 Calendar Tab 접속) 모든 변수 0으로 처리
        if user.id not in Leave.objects.filter(is_deleted=False, user_id=user.id).values_list('user_id', flat=True):
            count_available = Contact.objects.filter(user=user)\
                                             .annotate(count=Cast(Value(0), IntegerField()), fixed_annual_monthly_available=Cast(fixed_annual+fixed_monthly, IntegerField()),
                                                       days_remaining=Cast(Value(0), IntegerField()), this_month_count=Cast(Value(0), IntegerField()),
                                                       carry_over_usage_count=Cast(Value(0), IntegerField()))\
                                             .values('career', 'count', 'fixed_annual_monthly_available', 'days_remaining', 'this_month_count', 'carry_over_usage_count')
        else:
            count_available = Leave.objects.filter(is_deleted=False, user_id=user.id)\
                .annotate(monthly_count=Case(When(kind='Monthly', then=Value(1)), When(kind='morning_Half', then=Value(0.5)),
                                             When(kind='afternoon_Half', then=Value(0.5)), When(kind='Annual', then=Value(1)), output_field=FloatField()),
                          monthly_count_type2=Case(When(kind='carry_over', then=Value(1)), When(kind='carry_over_Half', then=Value(0.5)), output_field=FloatField()))\
                .values('user')\
                .annotate(career=F('user__contact__career'),
                          count=Coalesce(Sum(F('monthly_count'), filter=Q(from_date__gte=first_of_year, from_date__lte=last_of_year), output_field=FloatField()), 0, output_field=FloatField()),
                          carry_over_usage_count=Coalesce(Sum(F('monthly_count_type2'), filter=Q(from_date__gte=first_of_year, from_date__lte=last_of_year), output_field=FloatField()), 0, output_field=FloatField()),
                          fixed_annual_monthly_available=Cast(fixed_annual+fixed_monthly, IntegerField()),
                          days_remaining=ExpressionWrapper(F('fixed_annual_monthly_available')-F('count'), output_field=FloatField()),
                          this_month_count=Coalesce(Sum(F('monthly_count'), filter=Q(from_date__gte=first_day, from_date__lte=last_day), output_field=FloatField()), 0, output_field=FloatField()))\
                .values('career', 'count', 'carry_over_usage_count', 'fixed_annual_monthly_available', 'days_remaining', 'this_month_count')

        user_career = [];
        usage_count = []; # 사용 개수 (연/월차, 반차)
        carry_over_usage_count = []; # 사용 개수 (이월)
        fixed_annual_monthly_available = []; # 해당연도 사용 가능 개수
        days_remaining = []; # 해당연도 사용 가능 개수 - 사용 개수
        this_month_count = []; # 이번 달 사용 개수
        for available in count_available:
            user_career.append(available['career'])
            usage_count.append(float(available['count']))
            carry_over_usage_count.append(float(available['carry_over_usage_count']))
            fixed_annual_monthly_available.append(float(available['fixed_annual_monthly_available'])),
            days_remaining.append(available['days_remaining']),
            this_month_count.append((available['this_month_count']))

        last_year_leave = Leave.objects.filter(is_deleted=False, user_id=user.id, from_date__gte=datetime.date(today.year - 1, 1, 1), from_date__lte=datetime.date(today.year - 1, 12, 31)) \
            .annotate(monthly_count=Case(When(kind='Monthly', then=Value(1)), When(kind='morning_Half', then=Value(0.5)),
                                         When(kind='afternoon_Half', then=Value(0.5)), When(kind='Annual', then=Value(1)), output_field=FloatField())) \
            .values('user') \
            .annotate(LastYearFixedAnnualMonthly=Cast(lastYearFixedAnnual + lastYearFixedMonthly, IntegerField()),
                      count=Coalesce(Sum(F('monthly_count'), output_field=FloatField()), 0, output_field=FloatField()),
                      carry_over=ExpressionWrapper(F('LastYearFixedAnnualMonthly') - F('count'), output_field=FloatField()))

        # 사용 현황 Table - list
        user_leave = Leave.objects.filter(is_deleted=False, user_id=user.id, from_date__gte=first_of_year, from_date__lte=last_of_year).values('from_date', 'kind', 'name').order_by('-from_date')

        # 부재 정보 - 인수인계 Table
        research = Research.objects.filter(Q(is_deleted=0, is_recruiting='Recruiting'))

        # 정원 초과한 날 리스트 (하루 9명)
        #maximum_capacity = Leave.objects.filter(is_deleted=0, from_date_gte=datetime.today())\
        #                                .values('from_date') \
        #                                .annotate(capacity=Count('id', filter=(Q(user__groups__name='nurse') & (Q(kind='Annual') | Q(kind='Monthly')))))\
        #                                .filter(capacity__gte=9).values('from_date')
        limit = Leave.objects.filter(Q(is_deleted=False, from_date__gte=datetime.date(2025,6,1)) & (Q(kind='Monthly') | Q(kind='Annual'))) \
                                .values('from_date') \
                                .annotate(off=Count('user_id', filter=Q(user_id__groups__name='nurse'))) \
                                .filter(off__gte=Value(11)) \
                                .values_list('from_date', flat=True)
        limit_list = [];
        for limit in limit:
            limit_list.append(str(limit))

    else:
        fixed_annual = None
        last_year_leave = None
        research = Research.objects.filter(Q(is_deleted=0, is_recruiting='Recruiting'))

        return render(request, 'pages/leave/leave.html',
                      {'events': all_events, 'user': user, 'fixed_annual': fixed_annual, 'research': research, 'last_year_leave': last_year_leave})

    return render(request, 'pages/leave/leave.html', {'user_career': user_career, 'usage_count': usage_count, 'fixed_annual_monthly_available': fixed_annual_monthly_available,
                                                      'days_remaining': days_remaining, 'this_month_count': this_month_count, 'this_month': this_month, 'this_year': this_year,
                                                      'events': all_events, 'user': user, 'career_str': career_str, 'december_str': december_str,
                                                      'fixed_annual': fixed_annual, 'fixed_monthly': fixed_monthly, 'count_available': count_available,
                                                      'research': research, 'today': today, 'user_leave': user_leave, 'cal_career': cal_career, 'limit': limit_list,
                                                      'last_year_leave': last_year_leave, 'carry_over_usage_count': carry_over_usage_count})

# Display all events.
@login_required()
def all_events(request):
    all_events = Leave.objects.filter(Q(name='----마감----') | Q(is_deleted=0, user__is_active=True, from_date__isnull=False, name__isnull=False))
    out = []
    for event in all_events:
        out.append({
            'id': event.id,
            'memo': event.memo,
            'start': event.from_date.strftime("%Y-%m-%d"),
            'user_id': event.user_id,
            'title': event.name,
            'kind': event.kind,
            'from_date': event.from_date,
            'curr_user_id': request.user.id,
            'color': '#E5CCFF' if event.kind == 'Monthly' else '#CCE5FF' if event.kind == 'Annual' else '#CCFFE5' if event.kind in ['afternoon_Half', 'morning_Half'] else '#FFCCCC' if event.kind == 'official' else '#a3b4c1' if event.kind in ['carry_over', 'carry_over_Half'] else 'default_color'
        })

    return JsonResponse(out, safe=False)

# Update event.
@login_required()
def update(request, leave_id=None):
    if leave_id:
        instance = get_object_or_404(Leave, pk=leave_id)
    else:
        instance = Leave()

    form = LeaveForm(request, request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        return HttpResponseRedirect(reverse('leave:leave_calendar'))
    return render(request, 'pages/leave/leave_add.html', {'leave': instance,
                                                          'form': form})

# Remove event.
@login_required()
def remove(request, leave_id):
    leave = Leave.objects.get(pk=leave_id)
    leave.is_deleted = True
    leave.save()
    return HttpResponseRedirect(reverse('leave:leave_calendar'))

@login_required()
def leave_detail(request, leave_id):
    leave = Leave.objects.filter(pk=leave_id)\
                         .values('id', 'name', 'kind', 'from_date', 'memo', 'user__contact__id')
    research = Research.objects.filter(is_deleted=0, is_recruiting='Recruiting').prefetch_related('crc', 'first_backup', 'second_backup')
    return render(request, 'pages/leave/leave_detail.html', {'leave': leave, 'research': research})

@login_required()
def total_usage(request):
    today = datetime.date.today()
    onco_A = Contact.objects.filter(onco_A=1).values('user_id')
    december = datetime.date(today.year - 1, 12, 1)
    leave = Leave.objects.filter(is_deleted=0, user_id__in=onco_A, from_date__gte=datetime.date(today.year, 1, 1), from_date__lte=datetime.date(today.year, 12, 31))\
                        .annotate(count=Case(When(kind='Monthly', then=Value(1)), When(kind='morning_Half', then=Value(0.5)),
                                             When(kind='afternoon_Half', then=Value(0.5)), When(kind='Annual', then=Value(1)), output_field=FloatField()))\
                        .values('user').distinct().order_by('user__contact__career')\
                        .annotate(fixed_monthly=ExpressionWrapper(Value(12), output_field=IntegerField()),
                                  usage=Coalesce(Sum(F('count'), output_field=FloatField()), 0, output_field=FloatField()),
                                  before_december_available=ExpressionWrapper(Value(today.month), output_field=FloatField()))\
                        .values('user__first_name', 'user__contact__career', 'usage', 'before_december_available', 'fixed_monthly')

    return render(request, 'pages/leave/total_usage.html', {'leave': leave, 'december': december, 'today': today})


#class CalendarView(generic.ListView):
#    model = Patient
#    template_name = 'pages/leave/patient.html'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)

        # use today's date for the calendar / Patient Schedule & Personal Event
#        date = get_date(self.request.GET.get('month', None))
#        context['patient_prev_month'] = prev_month(date)
#        context['patient_next_month'] = next_month(date)
#        context['patient_get_month'] = get_month(date)
#        context['user'] = self.request.user
#        user = self.request.user

        # Instantiate our calendar class with today's year and date
#        cal = Calendar(date.year, date.month, user)
#        cal.setfirstweekday(6)

        # Call the formatmonth method, which returns our calendar as a table
#        html_cal = cal.formatmonth(date, withyear=True)
#        context['patient_calendar'] = mark_safe(html_cal)
#        context['patient'] = Patient.objects.filter(is_deleted=0)

#        return context

@login_required()
def event_update(request, patient_id=None):
    if patient_id:
        instance = get_object_or_404(Patient, pk=patient_id)
    else:
        instance = Patient()

    form = PatientForm(request, request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form = form.save(commit=False)
        form.user = request.user
        form.save()
        return HttpResponseRedirect(reverse('leave:patient_calendar'))
    return render(request, 'pages/leave/event/add.html', {'event': instance})

@login_required()
def patient_delete(request, patient_id):
    patient = Patient.objects.get(pk=patient_id)
    patient.is_deleted = True
    patient.save()
    return HttpResponseRedirect(f'/leave/patient/calendar/')

@login_required()
def patient_calendar(request):
    all_events = Patient.objects.filter(is_deleted=False)
    return render(request, 'pages/leave/patient.html', {'all_events': all_events})

# Display all events.
@login_required()
def patient_all_events(request):
    from_date = datetime.datetime.fromisoformat(request.GET.get('start'))
    to_date = datetime.datetime.fromisoformat(request.GET.get('end'))
    next_visit = Feedback.objects.filter(assignment__is_deleted=0, next_visit__isnull=False, next_visit__gte=from_date, next_visit__lte=to_date)\
                    .filter(Q(assignment__curr_crc__user_id=request.user.id) | Q(assignment__PI=request.user.first_name)) \
                    .values('assignment__id', 'next_visit', 'assignment__name', 'assignment__register_number')

    cycle_visit = Feedback.objects.filter(assignment__is_deleted=0, cycle__isnull=False, dosing_date__isnull=False, dosing_date__gte=from_date, dosing_date__lte=to_date)\
                    .filter(Q(assignment__curr_crc__user_id=request.user.id) | Q(assignment__PI=request.user.first_name)) \
                    .values('assignment__id', 'dosing_date', 'assignment__name', 'assignment__register_number', 'cycle', 'day')

    events = Patient.objects.filter(is_deleted=False, user=request.user)\
                            .annotate(end=ExpressionWrapper(F('end_date') + datetime.timedelta(days=1), output_field=DateField()))\
                            .values('id', 'from_date', 'end', 'title')

    visit_list = []
    for n_visit in next_visit:
        if not cycle_visit.filter(Q(assignment_id=str(n_visit['assignment__id']), dosing_date=str(n_visit['next_visit']))):
            visit_list.append({
                        'assignment_id': n_visit['assignment__id'],
                        'kind': 'next_visit',
                        'start': n_visit['next_visit'].strftime("%Y-%m-%d"),
                        'title': n_visit['assignment__name'] + ' ' + n_visit['assignment__register_number'],
                        'color': '#BAB1B1'
            })

    for c_visit in cycle_visit:
        visit_list.append({
                    'assignment_id': c_visit['assignment__id'],
                    'kind': 'cycle_visit',
                    'start': c_visit['dosing_date'].strftime("%Y-%m-%d"),
                    'title': c_visit['assignment__name'] + ' ' + c_visit['assignment__register_number'] + ' ' + c_visit['cycle'] if not c_visit['day'] else c_visit['assignment__name'] + ' ' + c_visit['assignment__register_number'] + ' C' + c_visit['cycle'] + 'D' + c_visit['day'],
                    'color': '#F2F595'
        })

    for event in events:
        visit_list.append({
                    'id': event['id'],
                    'kind': 'event',
                    'start': event['from_date'].strftime("%Y-%m-%d"),
                    'end': event['end'].strftime("%Y-%m-%d") if event['end'] else None,
                    'title': event['title'],
                    'from_date': event['from_date'],
                    'color': '#F77E82'
        })

    return JsonResponse(visit_list, safe=False)
