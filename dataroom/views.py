from .models import Image, Image_link, Page, protocol_upload, training_schedule, Material, MaterialCategory, \
    MaterialDownload, Educational_Material, Educational_Material_Download, GCPMaterial, GCPMaterialCategory, GCPMaterialDownload

from .forms import TrainingForm
from research.models import Research, ONCO_CR_COUNT, UploadFile, UploadEngFile, UploadInclusion, UploadExclusion, UploadReference
from feedback.models import Feedback, Assignment
from user.models import Contact

from django.views import generic
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.utils.safestring import mark_safe
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from datetime import datetime, timedelta, date
from calendar import HTMLCalendar
import calendar
from django.db.models import Q, Count, F, ExpressionWrapper, IntegerField, Value
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def searchdata(request):
    query = request.GET.get('cancer')

    image_link = Image_link.objects.all()
    page = Page.objects.filter(cancer=request.GET.get('cancer')).order_by('slide_number')

    today = datetime.today()
    from_date = datetime(today.year, today.month, 1)
    date_year = today.year
    date_month = today.month
    to_date = datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])
    EOT_assign = Feedback.objects.filter(assignment__is_deleted=0, cycle='EOT').values('assignment_id')
    EOS_assign = Feedback.objects.exclude(eos__isnull=True).values('assignment_id').distinct()  ##### 2024.03.07

    weekday = today.weekday()
    start_delta = timedelta(days=weekday, weeks=1)
    prev_start_of_week = today - start_delta
    prev_end_of_week = prev_start_of_week + timedelta(days=4)

    annotations = {}
    annotations['screening_filter'] = Count('research__assignment', distinct=True,
                                            filter=(Q(research__assignment__feedback__ICF_date__isnull=False) & Q(
                                                research__assignment__phase=F('m_target')) & Q(research__assignment__is_deleted=0) &
                                                    ~Q(research__assignment__status='pre-screening') & ~Q(
                                                        research__assignment__status='pre-screening-fail')))
    annotations['ongoing_filter'] = Count('research__assignment', distinct=True,
                                          filter=(Q(research__assignment__phase=F('m_target')) & Q(research__assignment__is_deleted=0) & ~Q(research__assignment__curr_crc__name='타기관') &
                                                  ((Q(research__assignment__feedback__cycle='1',
                                                      research__assignment__feedback__day='1',
                                                      research__assignment__feedback__dosing_date__gte=from_date) &
                                                    Q(research__assignment__feedback__cycle='EOT',
                                                      research__assignment__feedback__dosing_date__lt=to_date)) |
                                                   (Q(research__assignment__feedback__cycle='1',
                                                      research__assignment__feedback__day='1',
                                                      research__assignment__feedback__dosing_date__year=date_year) &
                                                    Q(research__assignment__feedback__cycle='1',
                                                      research__assignment__feedback__day='1',
                                                      research__assignment__feedback__dosing_date__month=date_month) &
                                                    ~Q(research__assignment__id__in=EOS_assign)) |
                                                   (Q(research__assignment__feedback__cycle='1',
                                                      research__assignment__feedback__day='1',
                                                      research__assignment__feedback__dosing_date__lt=from_date) &
                                                    ~Q(research__assignment__id__in=EOT_assign) & ~Q(research__assignment__id__in=EOS_assign)))))
    annotations['enroll_filter'] = Count('research__assignment', distinct=True,
                                         filter=(Q(research__assignment__feedback__cycle='1',
                                                   research__assignment__feedback__day='1') & Q(research__assignment__is_deleted=0) &
                                                 Q(research__assignment__phase=F('m_target'))))
    annotations['enroll_weekly_filter'] = Count('research__assignment', distinct=True,
                                                filter=(Q(research__assignment__feedback__cycle='1',
                                                          research__assignment__feedback__day='1',
                                                          research__assignment__phase=F('m_target'), research__assignment__is_deleted=0,
                                                          research__assignment__feedback__dosing_date__gte=prev_start_of_week,
                                                          research__assignment__feedback__dosing_date__lte=prev_end_of_week)))
    annotations['pre_screening_filter'] = Count('research__assignment', distinct=True,
                                                filter=((Q(research__assignment__status='pre-screening') | Q(
                                                    research__assignment__status='pre-screening-fail')) & Q(research__assignment__is_deleted=0) &
                                                        Q(research__assignment__feedback__ICF_date__isnull=False)))

    images = Image.objects.filter(research__is_deleted=False, cancer=request.GET.get('cancer')) \
        .values('research_id').distinct() \
        .annotate(**annotations) \
        .values(*annotations.keys(), 'id', 'research__research_name', 'research__is_pre_screening', 'research__id',
                'research__is_recruiting',
                'm_name', 'm_scr', 'm_ongo', 'm_enroll', 'm_target', 'cancer', 'slide_number')

    message = "{} 자료실".format(query)

    return render(request, 'pages/dataroom/data.html', {'message': message,
                                                        'images': images,
                                                        'image_link': image_link,
                                                        'page': page})


def detData(request, research_id):
    research = Research.objects.get(id=research_id)
    protocol = protocol_upload.objects.all()
    assignment_list = research.assignment_set.filter(Q(is_deleted=False) & ~Q(status='pre-screening') & ~Q(status='pre-screening-fail'))
    pre_assignment_list = research.assignment_set.filter(Q(is_deleted=False, status='pre-screening') | Q(is_deleted=False, status='pre-screening-fail'))

    # protocol_upload 에 있는 연구와 아닌 연구 구분하여 코드 작성 필요
    reference = protocol_upload.objects.filter(clinical_trial_id=research.id)
    for reference in reference:
        reference.reference = request.FILES.get('reference')
        reference.save()

    context = {
        'protocol': protocol,
        'research': research,
        'assignments': assignment_list,
        'pre_assignments': pre_assignment_list,
        'research_waiting_list': research.research_waitinglist_set.filter(is_deleted=False),
        'upload_files': UploadFile.objects.filter(is_deleted=False, research=research),
        'upload_engfiles': UploadEngFile.objects.filter(is_deleted=False, research=research),
        'upload_inclusions': UploadInclusion.objects.filter(is_deleted=False, research=research),
        'upload_exclusions': UploadExclusion.objects.filter(is_deleted=False, research=research),
        'upload_references': UploadReference.objects.filter(is_deleted=False, research=research),
    }
    return render(request, 'pages/dataroom/detailData.html', context)


def certification(request):
    materials = Material.objects.filter(is_deleted=0)
    categories = Material.get_categories()
    return render(request, 'pages/dataroom/training/certification.html', {'materials': materials,
                                                                          'categories': categories})


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def create_certification(request):
    is_update = request.POST.get('is_update')
    category = request.POST.get('category')
    name = request.POST.get('name')
    asset_number = None if request.POST.get('asset_number') == '' else request.POST.get('asset_number')
    year = request.POST.get('year')
    file = request.FILES.get('file')
    target_id = request.POST.get('target_id')
    if is_update == 'true':
        material = Material.objects.get(id=target_id)
        material.category = category
        material.name = name
        material.asset_number = asset_number
        material.year = year
        #material.update_date = timezone.now()
        if file is not None:
            material.materials = file
            material.materials_name = file.name
        material.save()
    else:
        new_material = Material(category=category, name=name, asset_number=asset_number, year=year, materials=file, materials_name=file.name, uploader=request.user)
        new_material.save()
    return HttpResponseRedirect('/dataroom/certification/')


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def delete_certification(request):
    target_id = request.POST.get('target_id')

    material = Material.objects.get(id=target_id)
    material.is_deleted = True
    material.save()
    return HttpResponseRedirect('/dataroom/certification/')


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def create_certification_category(request):
    category = request.POST.get('category')
    description = request.POST.get('description')

    new_material_category = MaterialCategory(category=category, description=description, uploader=request.user)
    new_material_category.save()
    return HttpResponseRedirect('/dataroom/certification/')


@require_http_methods(['POST'])
def download_certification(request):
    material_id = request.POST.get('materialId')

    new_material_download = MaterialDownload(
        downloader=request.user, material=Material.objects.get(pk=material_id))
    new_material_download.save()
    return HttpResponse()


def educational_material(request):
    materials = Educational_Material.objects.filter(is_deleted=0)
    return render(request, 'pages/dataroom/training/educational_material.html', {'materials': materials})


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def create_educational_material(request):
    is_update = request.POST.get('is_update')
    category = request.POST.get('category')
    version = request.POST.get('version')
    name = request.POST.get('name')
    file = request.FILES.get('file')
    target_id = request.POST.get('target_id')
    if is_update == 'true':
        material = Educational_Material.objects.get(id=target_id)
        material.category = category
        material.version = version
        material.name = name
        #material.update_date = timezone.now()
        if file is not None:
            material.materials = file
            material.materials_name = file.name
        material.save()
    else:
        new_material = Educational_Material(version=version, category=category, name=name, materials=file, materials_name=file.name, uploader=request.user)
        new_material.save()
    return HttpResponseRedirect('/dataroom/educational_material/')

@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def delete_educational_material(request):
    target_id = request.POST.get('target_id')

    material = Educational_Material.objects.get(id=target_id)
    material.is_deleted = True
    material.save()
    return HttpResponseRedirect('/dataroom/educational_material/')


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def update_educational_material(request):
    category = request.POST.get('category')
    version = request.POST.get('version')
    name = request.POST.get('name')
    file = request.FILES.get('file')

    target_id = request.POST.get('target_id')

    material = Educational_Material.objects.get(id=target_id)
    material.category = category
    material.version = version
    material.name = name
    material.file = file
    material.materials_name = file.name
    material.save()
    return HttpResponseRedirect('/dataroom/educational_material/')


@require_http_methods(['POST'])
def download_educational_material(request):
    material_id = request.POST.get('materialId')

    new_material_download = Educational_Material_Download(
        downloader=request.user, educational_material=Educational_Material.objects.get(pk=material_id))
    new_material_download.save()
    return HttpResponse()


@login_required()
def crc_check_list(request):
    training = training_schedule.objects.filter(is_deleted=0)
    return render(request, 'pages/dataroom/training/crc_check_list.html', {'training': training})


@login_required()
def all_events(request):
    from_date = datetime.fromisoformat(request.GET.get('start'))
    to_date = datetime.fromisoformat(request.GET.get('end'))
    all_events = training_schedule.objects.filter(is_deleted=0, date__gte=from_date, date__lte=to_date).values('id', 'memo', 'trainer', 'topic', 'location', 'date')
    out = []
    for event in all_events:
        out.append({
            'id': event['id'],
            'memo': event['memo'],
            'trainer': event['trainer'],
            'title': event['topic'],
            'location': event['location'],
            'start': event['date'].strftime("%Y-%m-%d %H:%M"),
        })

    return JsonResponse(out, safe=False)

def training(request, id=None):
    if id:
        instance = get_object_or_404(training_schedule, pk=id)
    else:
        instance = training_schedule()

    form = TrainingForm(request, request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form = form.save(commit=False)
        form.save()
        return HttpResponseRedirect(reverse('dataroom:crc_check_list'))
    return render(request, 'pages/dataroom/training/add.html', {'training': instance})

@login_required()
def training_delete(request, id):
    training = training_schedule.objects.get(pk=id)
    training.is_deleted = True
    training.save()
    return HttpResponseRedirect(f'/dataroom/crc/check_list/')


# GCP
def good_clinical_practice(request):
    materials = GCPMaterial.objects.filter(is_deleted=0)
    categories = GCPMaterial.get_categories()
    languages = GCPMaterial.field_value_and_text()
    seniors = Contact.objects.filter(is_senior=True).values_list('user_id', flat=True)

    return render(request, 'pages/dataroom/GCP/GCP.html', {'materials': materials, 'categories': categories, 'languages': languages, 'seniors': seniors})


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def create_good_clinical_practice(request):
    is_update = request.POST.get('is_update')
    category = request.POST.get('category')
    name = request.POST.get('name')
    year = request.POST.get('year')
    language = request.POST.get('language')
    file = request.FILES.get('file')
    target_id = request.POST.get('target_id')
    if is_update == 'true':
        material = GCPMaterial.objects.get(id=target_id)
        material.category = category
        material.name = name
        material.year = year
        material.language = language
        #material.update_date = timezone.now()
        if file is not None:
            material.materials = file
            material.materials_name = file.name
        material.save()
    else:
        new_material = GCPMaterial(category=category, name=name, year=year, language=language, materials=file, materials_name=file.name, uploader=request.user)
        new_material.save()
    return HttpResponseRedirect('/dataroom/good_clinical_practice/')


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def delete_good_clinical_practice(request):
    target_id = request.POST.get('target_id')

    material = GCPMaterial.objects.get(id=target_id)
    material.is_deleted = True
    material.save()
    return HttpResponseRedirect('/dataroom/good_clinical_practice/')


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def create_good_clinical_practice_category(request):
    category = request.POST.get('category')

    new_material_category = GCPMaterialCategory(category=category, uploader=request.user)
    new_material_category.save()
    return HttpResponseRedirect('/dataroom/good_clinical_practice/')


@require_http_methods(['POST'])
def download_good_clinical_practice(request):
    material_id = request.POST.get('materialId')

    new_material_download = GCPMaterialDownload(downloader=request.user, material=GCPMaterial.objects.get(pk=material_id))
    new_material_download.save()
    return HttpResponse()
