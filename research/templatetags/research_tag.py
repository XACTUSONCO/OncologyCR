import itertools, collections
from django import template
from django.db.models import Q, Max, Count, F, Value, Sum, ExpressionWrapper, FloatField, Case, When
from datetime import datetime, timedelta, date
from feedback.models import Assignment
import locale, re, calendar
from django.db.models.functions import Coalesce, Cast
from dateutil import relativedelta
from research.models import research_WaitingList
from user.models import Contact

register = template.Library()

@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    return str(dict_data.get(key))


@register.filter('get_m2m_values')
def get_m2m_values(m2m):
    ret = []
    for r in m2m:
        ret.append(getattr(r, 'value'))
    return ret

@register.filter('get_m2m_ids')
def get_m2m_ids(m2m):
    ret = []
    for r in m2m:
        ret.append(getattr(r, 'id'))
    return ret

@register.filter('get_m2m_names')
def get_m2m_names(m2m):
    ret = []
    for r in m2m:
        ret.append(getattr(r, 'name'))
    return ret

@register.filter('get_o2m_values')
def get_m2m_values(o2m):
    return getattr(o2m, 'value')

@register.filter
def get_value(list, key):
    return list[key]

@register.filter
def page_filter(queryset, cancer):
    return queryset.filter(cancer=cancer)

@register.filter
def chunks(value, chunk_length):
    """
    Breaks a list up into a list of lists of size <chunk_length>
    """
    clen = int(chunk_length)
    i = iter(value)
    while True:
        chunk = list(itertools.islice(i, clen))
        if chunk:
            yield chunk
        else:
            break

@register.filter
def is_numberic(value):
    return "{}".format(value).isdigit()

@register.filter
@register.simple_tag
def target_regex(value):
    numbers = re.sub(r'\([^)]*\)', '', value)
    numbers = re.findall('^([0-9]+)\+?\s?', numbers)
    if not numbers:
        return str(0)
    else:
        return numbers

@register.filter
@register.simple_tag
def enroll_percent(a,b):
    return round((a/int(b))*100)

@register.filter
@register.simple_tag
def visitor_percent(value, curr):
    return float(round((curr - value) / value * 100))

@register.filter
def change_korean(value):
    locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
    return datetime.strptime(str(value), '%Y-%m-%d').strftime('%a')

@register.filter
def cal_career(value):
    if value:
        today = date.today()
        return divmod((today - value).days, 365), divmod((today - value).days, 365)[1] // 30

@register.filter
def split(value, key):
    return value.split(key)

@register.filter
def subtract(value, arg):
    if value == '':
        value = 0.0
    if arg == '':
        arg = 0.0
    try:
        return float(value) - float(arg)
    except ValueError:
        return 0.0  # 기본값을 0.0으로 설정

@register.filter
def total_sum(value):
    value_list = [v[1:13] for v in value]
    return [sum(i) for i in zip(*value_list)]

@register.filter
def total_sum_by_team(value, team):
    value = [x for x in value if x[27] == team]
    value_list = [v[1:13] for v in value]
    return [sum(i) for i in zip(*value_list)]

@register.filter
def PMS_total_sum(value, team):
    value = [x for x in value if x[27] == team]
    value_list = [v[14:27] for v in value]
    return [sum(i) for i in zip(*value_list)]

#def sum_of_ongoings_by_PI_CRC(value, team):
#    list = [];
#    for v in value:
#        if v[0][1] == str(team):
#            list.append(v[1])
#            list = [[int(i) for i in x] for x in list]
#            sum_of_ongoings_by_PI_CRC = [sum(i) for i in zip(*list)]
#    return sum_of_ongoings_by_PI_CRC

@register.filter
@register.simple_tag
def sum_of_ongoings_by_PI_CRC(value):
    list = [];
    for v in value:
        list.append(v[1])
        list = [[int(i) for i in x] for x in list]
        sum_of_ongoings_by_PI_CRC = [sum(i) for i in zip(*list)]
    return sum_of_ongoings_by_PI_CRC

@register.filter
@register.simple_tag
def get_item(d, key):
    try:
        return d.get(key)
    except:
        return None

@register.filter
@register.simple_tag
def sum_of_ongoings_by_PI_CRC(value):
    list = [];
    for v in value:
        list.append(v[1])
        list = [[int(i) for i in x] for x in list]
        sum_of_ongoings_by_PI_CRC = [sum(i) for i in zip(*list)]
    return sum_of_ongoings_by_PI_CRC

@register.filter
@register.simple_tag
def get_my_team(request_user):
    try:
        my_team = Contact.objects.get(onco_A=1, user_id=request_user)
    except Contact.DoesNotExist:
        my_team = None
    return my_team

@register.filter
@register.simple_tag
def add_floats(value, arg):
    try:
        return value + float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
@register.simple_tag
def subtract_floats(value, arg):
    try:
        return value - float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
@register.simple_tag
def screening_target_filter(value, target):
    return value.filter(Q(ICF_date__isnull=False) & Q(assignment__phase=target) &
                        ~Q(assignment__status='pre-screening') & ~Q(assignment__status='pre-screening-fail'))\
        .values('assignment_id').distinct().count()

@register.filter
@register.simple_tag
def enroll_target_filter(value, target):
    return value.filter(Q(cycle='1', day='1') & Q(assignment__phase=target)).values('assignment_id').distinct().count()

@register.filter
def enroll_weekly_filter(value, target):
    today = datetime.today()
    weekday = today.weekday()
    start_delta = timedelta(days=weekday, weeks=1)
    prev_start_of_week = today - start_delta
    prev_end_of_week = prev_start_of_week + timedelta(days=4)
    return value.filter(cycle='1', day='1', dosing_date__gte=prev_start_of_week,
                        dosing_date__lte=prev_end_of_week, assignment__phase=target)\
        .values('assignment_id').distinct().count()

@register.filter
@register.simple_tag
def ongoing_total_filter(value, target):
        today = datetime.today()
        from_date = datetime(today.year, today.month, 1)
        date_year = today.year
        date_month = today.month
        to_date = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
        EOT_assign = value.filter(cycle='EOT').values('assignment_id')

        return value.filter(
            (Q(cycle='1', day='1', dosing_date__gte=from_date) & Q(cycle='EOT', dosing_date__lt=to_date)) |
            (Q(cycle='1', day='1', dosing_date__year=date_year) & Q(cycle='1', day='1', dosing_date__month=date_month)) |
            #(Q(cycle='EOT', dosing_date__gt=from_date) & Q(cycle='EOT', dosing_date__lte=to_date)) |
            (Q(cycle='1', day='1', dosing_date__lte=from_date) & ~Q(assignment_id__in=EOT_assign))
            ).filter(assignment__phase=target).values('assignment_id').distinct().count()

@register.filter
@register.simple_tag
def pre_screening_filter(value):
    return value.filter((Q(assignment__status='pre-screening') | Q(assignment__status='pre-screening-fail')) & Q(ICF_date__isnull=False)).values('id').distinct().count()

@register.filter
@register.simple_tag
def curr_waiting_filter(research_id, target):
    register_num_list = Assignment.objects.filter(is_deleted=0, research_id=research_id, phase=target) \
                                        .values('register_number') \
                                        .annotate(n_by_register_num=Count('register_number')) \
                                        .filter(n_by_register_num=1) \
                                        .values('register_number')

    return Assignment.objects.filter(is_deleted=0, research_id=research_id).filter(Q(status='pre-screening', register_number__in=register_num_list)).values('id').distinct().count()

@register.simple_tag
def count_available(value, user, career_year, career_month):
    today = datetime.date.today()

    first_of_year = datetime.date(today.year, 1, 1)
    last_of_year = datetime.date(today.year, 12, 31)
    first_day = datetime.date(today.year, today.month, 1)
    last_day = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    count_available = value.objects.filter(is_deleted=False, user_id=user, from_date__gte=first_of_year, from_date__lte=last_of_year)\
                    .annotate(monthly_count=Case(When(kind='Monthly', then=Value(1)), When(kind='morning_Half', then=Value(0.5)),
                                                 When(kind='afternoon_Half', then=Value(0.5)), When(kind='Annual', then=Value(1)), output_field=FloatField()))\
                    .values('user')\
                    .annotate(count=Coalesce(Sum(F('monthly_count'), output_field=FloatField()), 0, output_field=FloatField()),
                              before_december_available=(ExpressionWrapper(Value(today.month), output_field=FloatField())),
                              after_december_available=(ExpressionWrapper((today.year - career_year) * Value(12) + (today.month - career_month), output_field=FloatField())),
                              this_month_count=Coalesce(Sum(F('monthly_count'), filter=Q(from_date__gte=first_day, from_date__lte=last_day),
                                                    output_field=FloatField()), 0, output_field=FloatField())) \
                    .values('count', 'before_december_available', 'after_december_available', 'this_month_count')

    return count_available

@register.filter
@register.simple_tag
def fixed_annual(career):
    # 1개월 미만
    if (divmod((date.today() - career).days, 365)[0] == 0 and divmod((date.today() - career).days, 365)[1] // 30 == 0):
        return float(0)
    # 1개월 경과시
    elif (divmod((date.today() - career).days, 365)[0] == 0 and divmod((date.today() - career).days, 365)[1] // 30 <= 2):
        return float(1)
    # 3개월 경과시
    elif (divmod((date.today() - career).days, 365)[0] == 0 and divmod((date.today() - career).days, 365)[1] // 30 <= 5):
        return float(2)
    # 6개월 경과시
    elif (divmod((date.today() - career).days, 365)[0] == 0 and divmod((date.today() - career).days, 365)[1] // 30 <= 8):
        return float(3)
    # 9개월 경과시
    elif (divmod((date.today() - career).days, 365)[0] == 0 and divmod((date.today() - career).days, 365)[1] // 30 <= 12):
        return float(4)

    # 2년차
    elif divmod((date.today() - career).days, 365)[0] == 1 and divmod((date.today() - career).days, 365)[1] // 30 >= 0:
        return float(8)
    # 3년차
    elif divmod((date.today() - career).days, 365)[0] == 2 and divmod((date.today() - career).days, 365)[1] // 30 >= 0:
        return float(10)
    # 4년차
    elif divmod((date.today() - career).days, 365)[0] == 3 and divmod((date.today() - career).days, 365)[1] // 30 >= 0:
        return float(12)
    # 5년차 이상
    elif divmod((date.today() - career).days, 365)[0] >= 4 and divmod((date.today() - career).days, 365)[1] // 30 >= 0:
        return float(13)

@register.filter
@register.simple_tag
def after_december_available(career):
    return relativedelta.relativedelta(date.today(), career).months

@register.filter
@register.simple_tag
def at(lst, i):
    try: return lst[int(i)]
    except: return None
