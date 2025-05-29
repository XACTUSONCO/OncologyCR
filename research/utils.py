import collections
from .models import Research, UploadFile, Cancer, Alternation, \
    Lesion, Line, Chemotherapy, IO_Naive, Brain_METS, PDL1, Biopsy, History, \
    Phase, End_research
from django.db.models import Case, When, Value, IntegerField, Q, CharField
from itertools import chain

def create_research_field_change_summary(value):
    if isinstance(value, list):
        text = '['
        for v in value:
            text += str(v['show']) if 'show' in v else str(v)
            text += ', '
        text = text[:-2] + ']'
    else:
        text = str(value)
    return text


def generate_search_query(request):
    research_name = request.GET.get('research_name', '')
    research_name = None if research_name.strip() == '' else research_name
    study_code = request.GET.get('study_code', '')
    study_code = None if study_code.strip() == '' else study_code
    research_explanation = request.GET.get('research_explanation', '')
    research_explanation = None if research_explanation.strip() == '' else research_explanation
    #crc = request.GET.get('crc', '')
    #crc = None if crc.strip() == '' else crc
    crc = request.GET.getlist('crc', '')
    team = request.GET.get('team', '')
    team = None if team.strip() == '' else team
    PI = request.GET.get('PI', '')
    PI = None if PI.strip() == '' else PI
    medicine_name = request.GET.get('medicine_name', '')
    medicine_name = None if medicine_name.strip() == '' else medicine_name

    cancer = request.GET.getlist('cancer', [Cancer.NA])
    phase = request.GET.getlist('phase', [Phase.NA])
    type = request.GET.getlist('type')
    is_pre_screening = request.GET.get('is_pre_screening')
    #chemotherapy = request.GET.get('chemotherapy', Chemotherapy.NA)
    chemotherapy = request.GET.getlist('chemotherapy')
    lesion = request.GET.get('lesion', Lesion.NA)
    alternation = request.GET.getlist('alternation', [Alternation.NA])
    pdl1 = request.GET.get('pdl1', PDL1.NA)
    line = request.GET.get('line', Line.NA)
    io_naive = request.GET.get('io_naive', IO_Naive.NA)
    brain_mets = request.GET.get('brain_mets', Brain_METS.NA)
    biopsy = request.GET.get('biopsy', Biopsy.NA)

    register_number = request.GET.get('register_number', '')
    register_number = None if register_number.strip() == '' else register_number

    # Create Query
    query = Research.objects.filter(Q(is_deleted=False) & ~Q(status='종료보고완료') & ~Q(status='결과보고완료') & ~Q(status='장기보관완료')).annotate(
        custom_order=Case(
            When(is_recruiting='Recruiting', then=Value(1)), When(is_recruiting='Holding', then=Value(2)),
            When(is_recruiting='Not yet recruiting', then=Value(3)), When(is_recruiting='Completed', then=Value(4)), output_field=IntegerField())
                        ).order_by('custom_order').distinct()\
                        .prefetch_related('crc', 'cancer', 'phase', 'type', 'chemotherapy', 'alternation')        

    if research_name is not None:
        query = query.filter(research_name__icontains=research_name)
    if study_code is not None:
        query = query.filter(study_code__icontains=study_code)
    if research_explanation is not None:
        query = query.filter(research_explanation__icontains=research_explanation)
    #if crc is not None:
    #    query = query.filter(crc__icontains=crc)
    if crc:
        query = query.filter(Q(crc__user__id__in=crc, onco_A=1))

    if team is not None:
        query = query.filter(team__icontains=team)
    if PI is not None:
        query = query.filter(PI__icontains=PI)
    if medicine_name is not None:
        query = query.filter(medicine_name__icontains=medicine_name)

    if Cancer.NA not in cancer:
        query = query.filter(cancer__value__in=
                             set(cancer) | {Cancer.NA}).distinct()
    elif Cancer.NA in cancer and len(cancer) > 1:
        query = query.filter(cancer__value__in=cancer)
    if Phase.NA not in phase: # '해당없음' 또는 항목 값을 최소 1개 선택한 경우
        query = query.filter(phase__value__in=
                             set(phase) | {Phase.NA}).distinct()
    elif Phase.NA in phase and len(phase) > 1:
        query = query.filter(phase__value__in=phase)
    #if Phase.NA != phase:
    #    query = query.filter(phase__value__in={phase, Phase.NA})
    if type:
        query = query.filter(type__value__in=type)
    if is_pre_screening is not None:
        query = query.filter(is_pre_screening__in={is_pre_screening})
    #if Chemotherapy.NA != chemotherapy:
    #    query = query.filter(chemotherapy__value__in=
    #                         {chemotherapy, Chemotherapy.NA})
    #if Lesion.NA != lesion:
    #    query = query.filter(lesion__value__in={lesion, Lesion.NA})
    #if Alternation.NA not in alternation:
    #    query = query.filter(alternation__value__in=
    #                         set(alternation) | {Alternation.NA})
    if chemotherapy:
        query = query.filter(chemotherapy__value__in=chemotherapy)
    elif Alternation.NA in alternation and len(alternation) > 1:
        query = query.filter(alternation__value__in=alternation)

    if PDL1.NA != pdl1:
        query = query.filter(pdl1__value=pdl1)
    if Line.NA != line:
        query = query.filter(line__value__in={line, Line.NA})
    if IO_Naive.NA != io_naive:
        query = query.filter(io_naive__value=io_naive)
    if Brain_METS.NA != brain_mets:
        query = query.filter(brain_mets__value=brain_mets)
    if Biopsy.NA != biopsy:
        query = query.filter(biopsy__value=biopsy)

    if register_number is not None:
        query = query.filter(assignment__register_number__icontains=register_number)

    sort_q = request.GET.get('sort', 'custom_order')    # Search Research 탭 click 시 -> /research/search/ -> sort(X), custom_order(O)
    sort_q = 'id' if sort_q == '' else sort_q           # 따라서 sort_q('custom_order')
    query = query.order_by(sort_q, 'research_name')     # query.order_by('sort', 'custom_order', 'research_name') 

    query_dict = {
        'sort': sort_q,
        'research_name': research_name,
        'study_code': study_code,
        'research_explanation': research_explanation,
        'crc': crc,
        'team': team,
        'PI': PI,
        'medicine_name': medicine_name,
        'cancer': cancer,
        'phase': phase,
        'type': type,
        'is_pre_screening': is_pre_screening,
        'lesion': lesion,
        'alternation': alternation,
        'pdl1': pdl1,
        'line': line,
        'io_naive': io_naive,
        'brain_mets': brain_mets,
        'biopsy': biopsy,
        'chemotherapy': chemotherapy,
        'register_number': register_number
    }

    return query, query_dict


def compare_research_fields(prev_json, curr_json):
    comparing_field = [
        'is_recruiting',
        'is_pre_screening',
        'type',
        'route_of_administration',
        'status',
        'binder_location',
        'study_coordinator',
        'storage_date',
        'end_brief',
        'result_brief',
        'CRO',
        'CRA_name',
        'CRA_phoneNumber',
        'irb_number',
        'cris_number',
        'first_backup',
        'second_backup',
        'crc',
        'team',
        'PI',
        'contact',
        'research_name',
        'study_code',
        'research_explanation',
        'medicine_name',
        'arm_name',
        'cancer',
        'phase',
        'lesion',
        'alternation',
        'pdl1',
        'line',
        'chemotherapy',
        'io_naive',
        'brain_mets',
        'biopsy',
        'turn_around_time',
        'liver_function',
        'lung_function',
        'heart_function',
        'kidney_function',
        'remark'
    ]

    text_summary = {}
    for field_name in comparing_field:
        if field_name in prev_json and field_name in curr_json:
            if prev_json[field_name] != curr_json[field_name]:
                prev_summary = create_research_field_change_summary(
                    prev_json[field_name])
                curr_summary = create_research_field_change_summary(
                    curr_json[field_name])
                text_summary[field_name] = prev_summary + ' -> ' + curr_summary
        elif field_name not in prev_json and field_name in curr_json:
            curr_summary = create_research_field_change_summary(
                curr_json[field_name])
            text_summary[field_name] = 'None -> ' + curr_summary
        else:
            prev_summary = create_research_field_change_summary(
                prev_json[field_name])
            text_summary[field_name] = prev_summary + ' -> None'

    return text_summary


def generate_end_study_search_query(request):
    status = request.GET.get('status', '')
    status = None if status.strip() == '' else status
    research_name = request.GET.get('research_name', '')
    research_name = None if research_name.strip() == '' else research_name
    study_code = request.GET.get('study_code', '')
    study_code = None if study_code.strip() == '' else study_code
    PI = request.GET.get('PI', '')
    PI = None if PI.strip() == '' else PI

    # Create Query (Research 클래스 모델에 등록된 연구 중 종료보고, 결과보고, 장기보관완료된 연구)
    query_end_study = Research.objects.filter(is_deleted=0).filter(Q(status='종료보고완료') | Q(status='결과보고완료') | Q(status='장기보관완료')) \
                              .annotate(model_type=Case(When(id__in=Research.objects.filter(is_deleted=0).values_list('id', flat=True), then=Value('end_study')), output_field=CharField()))\
                              .values('id', 'status', 'research_name', 'study_code', 'PI', 'model_type', 'end_brief', 'result_brief', 'storage_date')\
                              .order_by('PI', 'research_name')

    if status is not None:
        query_end_study = query_end_study.filter(status=status)
    if research_name is not None:
        query_end_study = query_end_study.filter(research_name__icontains=research_name)
    if study_code is not None:
        query_end_study = query_end_study.filter(study_code__icontains=study_code)
    if PI is not None:
        query_end_study = query_end_study.filter(PI__icontains=PI)

    # Create Query (End_research 클래스 모델에 등록된 연구)
    query_end_research = End_research.objects.filter(is_deleted=0) \
                                     .annotate(model_type=Case(When(id__in=End_research.objects.filter(is_deleted=0).values_list('id', flat=True), then=Value('end_research')), output_field=CharField())) \
                                     .values('id', 'status', 'research_name', 'study_code', 'PI', 'model_type', 'end_brief', 'result_brief', 'storage_date') \
                                     .order_by('PI', 'research_name')

    if status is not None:
        query_end_research = query_end_research.filter(status=status)
    if research_name is not None:
        query_end_research = query_end_research.filter(research_name__icontains=research_name)
    if study_code is not None:
        query_end_research = query_end_research.filter(study_code__icontains=study_code)
    if PI is not None:
        query_end_research = query_end_research.filter(PI__icontains=PI)

    query = list(chain(query_end_study, query_end_research))

    query_dict = {
        'status': status,
        'research_name': research_name,
        'study_code': study_code,
        'PI': PI,
    }

    return query, query_dict
