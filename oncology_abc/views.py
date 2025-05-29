import datetime, calendar

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from feedback.models import Feedback
from datetime import timedelta, date
from django.db.models import F, When, Window
from django.db.models.functions import RowNumber
from administration.models import Notice
from leave.models import Leave
from research.models import Research
from user.models import Contact, InvestigatorContact
from django.db.models import Q, Count, Sum, Max, Case, When, IntegerField, Value
from dateutil import relativedelta

@login_required()
def index(request):
    today = datetime.datetime.today()
    today_str = today.strftime("%B %d, %Y")
    pre_seven_day = today - timedelta(days=7)
    pre_seven_day_str = pre_seven_day.strftime("%B %d, %Y")

    user_id = request.user.id

    notice_list = Notice.objects.filter(is_deleted=0, end_date__gt=today.now()).filter(Q(Q(target='ALL')) | Q(target=request.user.groups.first().name)) # Notifications

    study_status = Research.objects.filter(is_deleted=0, onco_A=1)\
                                    .values('is_recruiting') \
                                    .annotate(custom_order=Case(When(is_recruiting='Recruiting', then=Value(1)),
                                                                When(is_recruiting='Completed', then=Value(2)),
                                                                When(is_recruiting='Not yet recruiting', then=Value(3)),
                                                                When(is_recruiting='Holding', then=Value(4)),
                                                                output_field=IntegerField()))\
                                    .annotate(all=Count('id', distinct=True),
                                              my=Count('id', distinct=True, filter=(Q(crc__user_id=user_id, crc__user__first_name=request.user.first_name) | Q(PI=request.user.first_name)))) \
                                    .order_by('custom_order')

    my_ongoing_list = Research.objects.filter(is_deleted=0, onco_A=1, is_recruiting='Recruiting')\
                                      .filter(Q(crc__user_id=user_id, crc__user__first_name=request.user.first_name) | Q(PI=request.user.first_name))\
                                      .values('id').distinct().order_by('research_name')\
                                      .values('id', 'research_name')

    rec_scr = {
        pk
        for pk, row_no_in_group in Feedback.objects.filter(assignment__is_deleted=0, ICF_date__isnull=False).annotate(
                row_no_in_group=Window(
                expression=RowNumber(),
                partition_by=[F('assignment__research')],
                order_by=['assignment__research', F('ICF_date').asc(), 'assignment']
            )
        ).values_list('id', 'row_no_in_group')
        if row_no_in_group <= 2
    }
    rec_scr = Feedback.objects.filter(id__in=rec_scr, ICF_date__gte=pre_seven_day, ICF_date__lte=today)\
                              .values('assignment').order_by('-ICF_date')\
                              .values('assignment__id', 'assignment__status', 'assignment__name',
                                      'assignment__sex', 'assignment__age', 'assignment__no',
                                      'assignment__register_number', 'assignment__curr_crc__name', 'assignment__PI')

    leave = Leave.objects.filter(is_deleted=0, from_date=today, user__is_active=1) \
        .values('user_id__email').distinct() \
        .annotate(research_count=Count('user_id__email', filter=Q(user_id__email__in=Research.objects.filter(is_deleted=0, is_recruiting='Recruiting').values('crc__email')))) \
        .values('user_id__groups__name', 'user_id__email', 'kind', 'name', 'research_count')
    onco_A = Contact.objects.filter(onco_A=1).values_list('user_id', flat=True)

    # 최근 일주일간 데이터 입력자
    data_entry_in_the_last_week = Feedback.objects.filter(assignment__is_deleted=0, create_date__gte=pre_seven_day, create_date__lte=today)\
                               .values('uploader_id').distinct()
    # 현 종양내과 A팀 & 데이터 입력자 제외 & group name이 1.nurse 2.medeical records 중 하나인 직원
    no_data_entry_in_the_last_week = Contact.objects.filter(Q(onco_A=1) & ~Q(user_id__in=data_entry_in_the_last_week))\
                                     .filter(Q(user_id__groups__name='nurse') | Q(user_id__groups__name='medical records'))\
                                     .values('user_id', 'user__first_name')

    if Contact.objects.filter(user_id=user_id):
        research = Research.objects.filter(is_deleted=0, is_recruiting='Recruiting',
                                           crc__email__in=Leave.objects.filter(is_deleted=0, from_date=today).values('user_id__email'))\
                                    .distinct().order_by('research_name')\
                                    .prefetch_related('crc', 'first_backup', 'second_backup')
    else:
        research = None

    # 한 달간 등록 안된 연구
    stop_enroll = Research.objects.filter(is_deleted=0, is_recruiting='Recruiting', onco_A=True, PI=request.user.first_name)\
            .values('id') \
            .annotate(assignments=Sum(Case(When((Q(assignment__is_deleted=0) & ~Q(assignment__status='pre-screening') & ~Q(
            assignment__status='pre-screening-fail')), then=1), default=0, output_field=IntegerField())),
                    latest_enroll=Max('assignment__feedback__dosing_date', filter=Q(assignment__feedback__cycle='1', assignment__feedback__day='1')))\
            .filter(Q(assignments=0) |
                    Q(assignments__gte=1, latest_enroll__lte=date.today() - relativedelta.relativedelta(months=1)))\
            .values('PI', 'id', 'research_name', 'assignments', 'latest_enroll', 'create_date')\
            .order_by('PI', '-latest_enroll')

    return render(
        request, 'index.html', {
            'today': today_str,
            'rec_scr': rec_scr,
            'pre_seven_day': pre_seven_day_str,
            'research': research,
            'leave': leave,
            'user_id': user_id,
            'onco_A': onco_A,
            'field_choice': Leave.field_value_and_text(),
            'no_data_entry_in_the_last_week': no_data_entry_in_the_last_week,
            'stop_enroll': stop_enroll,
            'notice_list': notice_list,
            'study_status': study_status,
            'my_ongoing_list': my_ongoing_list
        }
    )
