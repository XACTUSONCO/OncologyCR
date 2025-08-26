import datetime, calendar
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q, Value, When, IntegerField, Case, FloatField, Sum, F, ExpressionWrapper, DateField, DurationField, Count
from django.db.models.functions import Coalesce, Cast
from django.contrib.auth.decorators import login_required

from research.models import Research
from user.models import Contact
from feedback.models import Feedback
from .forms import LeaveForm, PatientForm
from .models import Leave, Patient


# Create your views here.
@login_required()
def leave_calendar(request):
    all_events = Leave.objects.filter(is_deleted=False)
    user = request.user
    today = datetime.date.today()
    this_month = today.month
    this_year = today.year
    contact = Contact.objects.filter(user=user).first()

    # is_doctor = user.groups.filter(name='doctor').exists()
    # oncoA = contact.onco_A if contact else False
    #
    # if not (is_doctor or oncoA):
    #     return redirect('/')  # 또는 return HttpResponseForbidden()

    if contact:
        # 연/월차
        fixed_annual = contact.get_fixed_annual()
        fixed_monthly = contact.get_fixed_monthly()

        career_str = contact.career.strftime('%Y-%m-%d') if contact.career else ''
        december_str = datetime.date(today.year - 1, 12, 1).strftime('%Y-%m-%d')

        # 작년 기준 이월 연차/월차 (이월휴가 계산용)
        last_year_ref = datetime.date(today.year - 1, 12, 31)
        LastYearFixedAnnual = contact.get_fixed_annual(reference_date=last_year_ref)
        LastYearFixedMonthly = contact.get_fixed_monthly(reference_date=last_year_ref)

        # 일 년의 첫 날과 마지막 날
        first_of_year = datetime.date(today.year, 1, 1)
        last_of_year = datetime.date(today.year, 12, 31)
        # 한 달의 첫 날과 마지막 날
        first_day = datetime.date(today.year, today.month, 1)
        last_day = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        # 사용 현황
        used_leave_days = Leave.objects.filter(is_deleted=False, user_id=user.id, from_date__range=(first_of_year, last_of_year))\
                                    .values('from_date', 'kind')\
                                    .order_by('-from_date')

        if not Leave.objects.filter(is_deleted=False, user_id=user.id).exists():
            # 신규자 등 휴가가 아직 등록되지 않은 경우: 모두 0
            count_available = Contact.objects.filter(user=user)\
                                             .annotate(usage_count=Cast(Value(0), IntegerField()),
                                                       fixed_annual_monthly_available=Cast(fixed_annual+fixed_monthly, IntegerField()),
                                                       days_remaining=Cast(Value(0), IntegerField()),
                                                       this_month_count=Cast(Value(0), IntegerField()),
                                                       carry_over_usage_count=Cast(Value(0), IntegerField()))\
                                             .values('career', 'usage_count', 'fixed_annual_monthly_available', 'days_remaining', 'this_month_count', 'carry_over_usage_count')
        else:
            count_available = Leave.objects.filter(is_deleted=False, user_id=user.id).annotate(\
                        # 월차/연차/반차
                        monthly_count=Case(When(kind='Monthly', then=Value(1)),
                                           When(kind='morning_Half', then=Value(0.5)),
                                           When(kind='afternoon_Half', then=Value(0.5)),
                                           When(kind='Annual', then=Value(1)),
                                           output_field=FloatField()),
                        # 이월
                        monthly_count_type2=Case(When(kind='carry_over', then=Value(1)),
                                                 When(kind='carry_over_Half', then=Value(0.5)),
                                                 output_field=FloatField()))\
                .values('user').annotate(\
                        career=F('user__contact__career'), # 입사일
                        usage_count=Coalesce(Sum(F('monthly_count'),
                                        filter=Q(from_date__range=(first_of_year, last_of_year)), output_field=FloatField()), 0, output_field=FloatField()), # 한 해 사용일수 (연/월/반차)
                        carry_over_usage_count=Coalesce(Sum(F('monthly_count_type2'),
                                        filter=Q(from_date__range=(first_of_year, last_of_year)), output_field=FloatField()), 0, output_field=FloatField()), # 한 해 사용일수 (이월)
                        fixed_annual_monthly_available=Cast(fixed_annual+fixed_monthly, IntegerField()), # 사용 가능한 휴가일수
                        days_remaining=ExpressionWrapper(F('fixed_annual_monthly_available')-F('usage_count'), output_field=FloatField()), # 남은 휴가일수
                        this_month_count=Coalesce(Sum(F('monthly_count'),
                                        filter=Q(from_date__range=(first_day, last_day)), output_field=FloatField()), 0, output_field=FloatField()) # 이번달 사용일수
                )\
                .values('career', 'usage_count', 'carry_over_usage_count', 'fixed_annual_monthly_available', 'days_remaining', 'this_month_count')

        user_career = []; # 입사일
        usage_count = []; # 한 해 사용일수 (연/월/반차)
        carry_over_usage_count = []; # 한 해 사용일수 (이월)
        fixed_annual_monthly_available = []; # 사용 가능한 휴가일수
        days_remaining = []; # 남은 휴가일수
        this_month_count = []; # 이번달 사용일수
        for available in count_available:
            user_career.append(available['career'])
            usage_count.append(float(available['usage_count']))
            carry_over_usage_count.append(float(available['carry_over_usage_count']))
            fixed_annual_monthly_available.append(float(available['fixed_annual_monthly_available'])),
            days_remaining.append(available['days_remaining']),
            this_month_count.append((available['this_month_count']))

        # 이월
        carry_over = Leave.objects.filter(is_deleted=False, user_id=user.id,
                                          from_date__range=(datetime.date(today.year-1, 1, 1), datetime.date(today.year-1, 12, 31))) \
            .annotate(monthly_count=Case(When(kind='Monthly', then=Value(1)),
                                         When(kind='morning_Half', then=Value(0.5)),
                                         When(kind='afternoon_Half', then=Value(0.5)),
                                         When(kind='Annual', then=Value(1)),
                                         output_field=FloatField())) \
            .values('user') \
            .annotate(LastYearFixedAnnualMonthly=Cast(LastYearFixedAnnual + LastYearFixedMonthly, IntegerField()), # 전년도 기준 사용 가능한 휴가일수
                      usage_count=Coalesce(Sum(F('monthly_count'), output_field=FloatField()), 0, output_field=FloatField()), # 전년도 사용일수
                      carry_over=ExpressionWrapper(F('LastYearFixedAnnualMonthly') - F('usage_count'), output_field=FloatField()) # 이월 휴가일수
                      )

        carry_over_value = carry_over[0]['carry_over'] if carry_over else 0
        carry_over_used = carry_over_usage_count[0] if carry_over_usage_count else 0

        # 3월 31일까지 사용하지 않은 이월 휴가는 소멸
        carry_over_valid_until = datetime.date(today.year, 3, 31)
        if today > carry_over_valid_until:
            effective_carry_over = 0  # 3월 31일 이후면 이월 휴가는 소멸 (무조건 0)
        else:
            effective_carry_over = max(carry_over_value - carry_over_used, 0)  # 그전이면 아직 사용하지 않은 이월만큼 사용 가능

    else:
        fixed_annual = None
        carry_over_value = None


        return render(request, 'pages/leave/leave.html',
                      {'events': all_events,
                       'user': user,
                       'fixed_annual': fixed_annual,
                       'carry_over_value': carry_over_value
                       })

    return render(request, 'pages/leave/leave.html', {'user_career': user_career,
                                                      'usage_count': usage_count,
                                                      'fixed_annual_monthly_available': fixed_annual_monthly_available,
                                                      'days_remaining': days_remaining,
                                                      'this_month_count': this_month_count,
                                                      'this_month': this_month,
                                                      'this_year': this_year,
                                                      'events': all_events,
                                                      'user': user,
                                                      'career_str': career_str,
                                                      'december_str': december_str,
                                                      'fixed_annual': fixed_annual,
                                                      'fixed_monthly': fixed_monthly,
                                                      'count_available': count_available,
                                                      'today': today,
                                                      'used_leave_days': used_leave_days,
                                                      'cal_career': contact.get_career_duration(),
                                                      'carry_over_value': carry_over_value,
                                                      'effective_carry_over': effective_carry_over,
                                                      'carry_over_usage_count': carry_over_usage_count})

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

# @login_required()
# def total_usage(request):
#     today = datetime.date.today()
#     onco_A = Contact.objects.filter(onco_A=1).values('user_id')
#     december = datetime.date(today.year - 1, 12, 1)
#     leave = Leave.objects.filter(is_deleted=0, user_id__in=onco_A, from_date__gte=datetime.date(today.year, 1, 1), from_date__lte=datetime.date(today.year, 12, 31))\
#                         .annotate(count=Case(When(kind='Monthly', then=Value(1)), When(kind='morning_Half', then=Value(0.5)),
#                                              When(kind='afternoon_Half', then=Value(0.5)), When(kind='Annual', then=Value(1)), output_field=FloatField()))\
#                         .values('user').distinct().order_by('user__contact__career')\
#                         .annotate(fixed_monthly=ExpressionWrapper(Value(12), output_field=IntegerField()),
#                                   usage=Coalesce(Sum(F('count'), output_field=FloatField()), 0, output_field=FloatField()),
#                                   before_december_available=ExpressionWrapper(Value(today.month), output_field=FloatField()))\
#                         .values('user__first_name', 'user__contact__career', 'usage', 'before_december_available', 'fixed_monthly')
#
#     return render(request, 'pages/leave/total_usage.html', {'leave': leave, 'december': december, 'today': today})

def total_usage(request):
    today = datetime.date.today()

    contacts = Contact.objects.filter(onco_A=True).select_related('user').order_by('career')

    results = []
    for c in contacts:
        # 사용 내역 집계
        leave_filter = Q(is_deleted=False, user=c.user,
                         from_date__range=(datetime.date(today.year, 1, 1),
                                           datetime.date(today.year, 12, 31)))

        usage = Leave.objects.filter(leave_filter).annotate(
            count=Case(
                When(kind='Monthly', then=Value(1)),
                When(kind='morning_Half', then=Value(0.5)),
                When(kind='afternoon_Half', then=Value(0.5)),
                When(kind='Annual', then=Value(1)),
                output_field=FloatField()
            )
        ).aggregate(total=Coalesce(Sum('count', output_field=FloatField()), 0.0))['total']

        # ✅ Contact 메서드 활용
        fixed_annual = c.get_fixed_annual(today)
        fixed_monthly = c.get_fixed_monthly(today)

        available = fixed_annual + fixed_monthly
        remaining = available - usage

        results.append({
            "name": c.user.first_name,
            "career": c.get_career_duration(today),
            "fixed_annual": fixed_annual,
            "fixed_monthly": fixed_monthly,
            "available": available,
            "usage": usage,
            "remaining": remaining,
        })

    return render(request, "pages/leave/total_usage.html", {
        "leave": results,
        "today": today,
    })


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
