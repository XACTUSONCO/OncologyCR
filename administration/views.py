import os
from datetime import datetime, date, timedelta
from itertools import groupby

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.core.exceptions import SuspiciousOperation
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from reportlab.platypus import SimpleDocTemplate, Table

from administration.models import Notice, Organization, Company, Commute
from administration.utils import daterange
from dataroom.models import Page, Image_link, Image
from research.models import Study_Category, Study_SubCategory, Research, ONCO_CR_COUNT
from user.models import Contact
from user.models import Team, Location
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

CANCERS = (
    'Breast',    
    'Stomach',
    'Sarcoma',
    'CRC',
    'Urological',
    'Lung',
    'Melanoma',
    'Phase1',
    'Pancreatic')


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def organization(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/organization.html',
                      {'organizations': Organization.objects.filter(is_deleted=False)})
    elif request.method == 'POST':
        name = request.POST.get('name')
        image = request.FILES.get('image')
        is_deleted = request.POST.get('is_deleted')
        is_update = request.POST.get('is_update')
        organization_id = request.POST.get('organization_id')
        if is_update == 'true':
            updated_organization = Organization.objects.get(pk=organization_id)
            updated_organization.name = name
            if image is not None:
                updated_organization.logo = image
            elif is_deleted:
                updated_organization.logo = None
            updated_organization.save()
        else:
            new_organization = Organization(name=name, logo=image)
            new_organization.save()
        return HttpResponseRedirect('/administration/organization/')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def organization_delete(request):
    organization_ids = request.POST.get('organization_ids')
    Organization.objects.filter(id__in=organization_ids.split(',')).update(is_deleted=True)
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def user(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/user.html',
                      {'users': User.objects.select_related('contact').all(), 'groups': Group.objects.all(),
                          'locations': Location.objects.all(), 'teams': Team.objects.all})
    elif request.method == 'POST' and request.POST.get('is_update') == 'true':
        user_id = request.POST.get('user_id')
        username = request.POST.get('username') or None
        email = request.POST.get('email') or ""
        name = request.POST.get('name') or None
        eng_name = request.POST.get('eng_name') or None
        phone = request.POST.get('phone') or None
        work_phone = request.POST.get('work_phone') or None
        career = request.POST.get('career') or None
        career_end = request.POST.get('career_end') or None
        groups = request.POST.getlist('groups') or None
        team = request.POST.get('team') or None
        location = request.POST.get('location') or None
        active = request.POST.get('active') or None
        onco_A = request.POST.get('onco_A') or None
        is_senior = request.POST.get('is_senior') or None

        User.objects.filter(id=user_id).update(username=username, email=email, is_active=active == "Y")
        updated_user = User.objects.get(id=user_id)
        if groups is not None:
            updated_user.groups.clear()
            for group in groups:
                new_group = Group.objects.get(name=group)
                new_group.user_set.add(updated_user)
        Contact.objects.get_or_create(user=updated_user)
        Contact.objects.filter(user_id=user_id).update(name=name, eng_name=eng_name, phone=phone, work_phone=work_phone,
                                                       career=career, career_end=career_end, onco_A=True if onco_A == 'Y' else False,
                                                       is_senior=True if is_senior == 'Y' else False,
                                                       team=Team.objects.get(name=team) if team is not None else None,
                                                       location=Location.objects.get(name=location) if location is not None else None),
        return render(request, 'pages/administration/user.html',
                      {'users': User.objects.select_related('contact').all(), 'groups': Group.objects.all(),
                       'locations': Location.objects.all(), 'teams': Team.objects.all})
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def user_group(request):
    try:
        if request.method == 'GET':
            return render(request, 'pages/administration/user_group.html',
                          {'groups': Group.objects.all()})
        elif request.method == 'POST':
            name = request.POST.get('name')
            is_update = request.POST.get('is_update')
            group_id = request.POST.get('group_id')
            if is_update == 'true':
                updated_group = Group.objects.get(pk=group_id)
                updated_group.name = name
                updated_group.save()
            else:
                new_group = Group(name=name)
                new_group.save()
            return HttpResponseRedirect('/administration/user/group/')
        else:
            raise SuspiciousOperation("Invalid request")
    except:
        return HttpResponseRedirect('/administration/user/group/')


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def user_group_delete(request):
    group_ids = request.POST.get('group_ids')
    Group.objects.filter(id__in=group_ids.split(',')).delete()
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def user_team(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/user_team.html',
                      {'teams': Team.objects.all()})
    elif request.method == 'POST':
        name = request.POST.get('name')
        is_update = request.POST.get('is_update')
        team_id = request.POST.get('team_id')
        if is_update == 'true':
            updated_team = Team.objects.get(pk=team_id)
            updated_team.name = name
            updated_team.save()
        else:
            new_team = Team(name=name)
            new_team.save()
        return HttpResponseRedirect('/administration/user/team/')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def user_team_delete(request):
    team_ids = request.POST.get('team_ids')
    Team.objects.filter(id__in=team_ids.split(',')).delete()
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def user_location(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/user_location.html',
                      {'locations': Location.objects.all()})
    elif request.method == 'POST':
        name = request.POST.get('name')
        is_update = request.POST.get('is_update')
        location_id = request.POST.get('location_id')
        if is_update == 'true':
            updated_location = Location.objects.get(pk=location_id)
            updated_location.name = name
            updated_location.save()
        else:
            new_location = Location(name=name)
            new_location.save()
        return HttpResponseRedirect('/administration/user/location/')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def user_location_delete(request):
    location_ids = request.POST.get('location_ids')
    Location.objects.filter(id__in=location_ids.split(',')).delete()
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def company(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/company.html',
                      {'companies': Company.objects.filter(is_deleted=False)})
    elif request.method == 'POST':
        type = request.POST.get('type')
        name_eng = request.POST.get('name_eng')
        name_kor = request.POST.get('name_kor')
        foreign_type = request.POST.get('foreign_type')
        is_update = request.POST.get('is_update')
        company_id = request.POST.get('company_id')
        if is_update == 'true':
            updated_company = Company.objects.get(pk=company_id)
            updated_company.type = type
            updated_company.name_eng = name_eng
            updated_company.name_kor = name_kor
            updated_company.foreign_type = foreign_type
            updated_company.save()
        else:
            new_company = Company(type=type, name_eng=name_eng, name_kor=name_kor, foreign_type=foreign_type)
            new_company.save()
        return HttpResponseRedirect('/administration/company/')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def company_delete(request):
    company_ids = request.POST.get('company_ids')
    Company.objects.filter(id__in=company_ids.split(',')).update(is_deleted=True)
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def study_set_up(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/study_set_up.html',
                      {'study_categories': Study_Category.objects.raw(
                          'select a.id, a.name, (select group_concat(name separator ", ") from research_study_subcategory as b where b.category_id = a.id) as sub_categories from research_study_category as a;')})
    elif request.method == 'POST':
        name = request.POST.get('name')
        new_study_category = Study_Category(name=name)
        new_study_category.save()
        return HttpResponseRedirect('/administration/study_set_up/')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def study_set_up_delete(request):
    study_category_ids = request.POST.get('study_category_ids')
    Study_Category.objects.filter(id__in=study_category_ids.split(',')).delete()
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def study_set_up_subcategory(request, study_category_id):
    if request.method == 'GET':
        return render(request, 'pages/administration/study_set_up_subcategory.html',
                      {
                          'study_category': Study_Category.objects.get(id=study_category_id),
                          'study_subcategories': Study_SubCategory.objects.filter(category_id=study_category_id)})
    elif request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        order = request.POST.get('order')
        study_subcategory_id = request.POST.get('study_subcategory_id')
        is_update = request.POST.get('is_update')
        if is_update == 'true':
            updated_sub_category = Study_SubCategory.objects.get(pk=study_subcategory_id)
            updated_sub_category.name = name
            updated_sub_category.description = description
            updated_sub_category.order = order
            updated_sub_category.save()
        else:
            new_study_subcategory = Study_SubCategory(name=name, description=description, order=order,
                                                      category_id=study_category_id)
            new_study_subcategory.save()

        return HttpResponseRedirect(f'/administration/study_set_up/{study_category_id}')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def study_set_up_subcategory_delete(request):
    study_subcategory_ids = request.POST.get('study_subcategory_ids')
    Study_SubCategory.objects.filter(id__in=study_subcategory_ids.split(',')).delete()
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def cancer_image_set_up(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/cancer_image_set_up.html',
                      {'pages': Page.objects.all(),
                       'cancers': CANCERS})
    elif request.method == 'POST':
        page_id = request.POST.get('page_id')
        cancer = request.POST.get('cancer')
        slide_number = request.POST.get('slide_number')
        slide = request.FILES.get('slide')
        is_update = request.POST.get('is_update')
        is_deleted = request.POST.get('is_deleted')
        if is_update == 'true':
            page = Page.objects.get(pk=page_id)
            page.cancer = cancer
            page.slide_number = slide_number
            if slide is not None:
                page.slide = slide
            elif is_deleted:
                page.slide = None
            page.save()
        else:
            new_page = Page(cancer=cancer, slide_number=slide_number, slide=slide)
            new_page.save()

        return HttpResponseRedirect('/administration/cancer_image_set_up')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def cancer_image_set_up_delete(request):
    page_ids = request.POST.get('page_ids')
    Page.objects.filter(id__in=page_ids.split(',')).delete()
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def cancer_image_set_up_image_links(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/cancer_image_set_up_image_links.html',
                      {'image_links': Image_link.objects.prefetch_related('clinical_trial', 'clinical_trial__research'),
                       'images': Image.objects.prefetch_related('research').order_by('research__research_name')})
    elif request.method == 'POST':
        image_link_id = request.POST.get('imagelink_id')
        clinical_trial = request.POST.get('clinical_trial')
        link_top = request.POST.get('link_top')
        link_left = request.POST.get('link_left')
        link_right = request.POST.get('link_right')
        link_bottom = request.POST.get('link_bottom')
        is_update = request.POST.get('is_update')
        if is_update == 'true':
            image_link = Image_link.objects.get(pk=image_link_id)
            image_link.clinical_trial_id = clinical_trial
            image_link.link_top = link_top
            image_link.link_left = link_left
            image_link.link_right = link_right
            image_link.link_bottom = link_bottom
            image_link.save()
        else:
            new_image_link = Image_link(clinical_trial_id=clinical_trial, link_top=link_top, link_left=link_left,
                                        link_right=link_right, link_bottom=link_bottom)
            new_image_link.save()

        return HttpResponseRedirect('/administration/cancer_image_set_up/image_links/')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def cancer_image_set_up_image_links_delete(request):
    imagelink_ids = request.POST.get('imagelink_ids')
    Image_link.objects.filter(id__in=imagelink_ids.split(',')).delete()
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def cancer_image_set_up_images(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/cancer_image_set_up_images.html',
                      {'images': Image.objects.prefetch_related('research'),
                       'researchs': Research.objects.filter(is_deleted=False).values('id', 'research_name').order_by('research_name'),
                       'cancers': CANCERS,
                       'targets': ONCO_CR_COUNT.objects.order_by('research__research_name').prefetch_related('research')})
    elif request.method == 'POST':
        image_id = request.POST.get('image_id')
        research_id = request.POST.get('research')
        m_name = request.POST.get('m_name')
        m_scr = request.POST.get('m_scr')
        m_ongo = request.POST.get('m_ongo')
        m_enroll = request.POST.get('m_enroll')
        m_target = request.POST.get('m_target')
        cancer = request.POST.get('cancer')
        slide_number = request.POST.get('slide_number')
        is_update = request.POST.get('is_update')
        if is_update == 'true':
            image = Image.objects.get(pk=image_id)
            image.research_id = research_id
            image.m_name = m_name
            image.m_scr = m_scr
            image.m_ongo = m_ongo
            image.m_enroll = m_enroll
            image.m_target = m_target
            image.cancer = cancer
            image.slide_number = slide_number
            image.save()
        else:
            new_image = Image(research_id=research_id,
                              m_name=m_name,
                              m_scr=m_scr,
                              m_ongo=m_ongo,
                              m_enroll=m_enroll,
                              m_target=m_target,
                              cancer=cancer,
                              slide_number=slide_number)
            new_image.save()

        return HttpResponseRedirect('/administration/cancer_image_set_up/images/')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def cancer_image_set_up_images_delete(request):
    image_ids = request.POST.get('image_ids')
    Image.objects.filter(id__in=image_ids.split(',')).delete()
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET', 'POST'])
def notice(request):
    if request.method == 'GET':
        return render(request, 'pages/administration/notice.html',
                      {'notices': Notice.objects.filter(is_deleted=False), 'groups': Group.objects.all()})
    elif request.method == 'POST':
        fmt = "%Y-%m-%d %H:%M"
        title = request.POST.get('title')
        contents = request.POST.get('contents')
        target = request.POST.get('target')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date_fmt = datetime.strptime(start_date, fmt)
        end_date_fmt = datetime.strptime(end_date, fmt)
        is_update = request.POST.get('is_update')
        notice_id = request.POST.get('notice_id')
        if is_update == 'true':
            updated_notice = Notice.objects.get(pk=notice_id)
            updated_notice.title = title
            updated_notice.contents = contents
            updated_notice.target = target
            updated_notice.start_date = start_date_fmt
            updated_notice.end_date = end_date_fmt
            updated_notice.save()
        else:
            new_notice = Notice(title=title, contents=contents, target=target,
                                start_date=start_date_fmt,
                                end_date=end_date_fmt,
                                user=request.user)
            new_notice.save()
        return HttpResponseRedirect('/administration/notice/')
    else:
        raise SuspiciousOperation("Invalid request")


@csrf_exempt
@login_required()
@require_http_methods(['POST'])
def notice_delete(request):
    notice_ids = request.POST.get('notice_ids')
    Notice.objects.filter(id__in=notice_ids.split(',')).update(is_deleted=True)
    return HttpResponse()


@csrf_exempt
@login_required()
@require_http_methods(['GET'])
def commute(request):
    return render(request, 'pages/administration/commute.html',
                  {'commutes': Commute.objects.all()})


@login_required()
def download_commute_excel(request):
    min = request.GET.get('min')
    max = request.GET.get('max')

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = 'commute_list_' + filename

    workbook = Workbook()
    worksheet = workbook.active

    users = User.objects.all()
    usernames = list(users.values_list('username', flat=True))

    worksheet.append([''] + usernames)

    commutes = Commute.objects.filter(date__gte=min, date__lte=max)
    commutes_by_username = groupby(commutes, key=lambda c: c.user.username)

    commutes_set = {}
    for username, group in commutes_by_username:
        commutes_set[username] = set(c.date for c in group)

    for single_date in daterange(datetime.strptime(min, '%Y-%m-%d'), datetime.strptime(max, '%Y-%m-%d')):
        row = [single_date]
        for username in usernames:
            try:
                if single_date in commutes_set[username]:
                    row.append('Y')
                else:
                    row.append('N')
            except KeyError:
                row.append('N')
        worksheet.append(row)

    response = HttpResponse(
        content=save_virtual_workbook(workbook),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = \
        'attachment; filename=' + filename + '.xlsx'
    return response


@login_required()
def download_commute_pdf(request):
    min = request.GET.get('min')
    max = request.GET.get('max')

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = 'commute_list_' + filename

    users = User.objects.all()
    usernames = list(users.values_list('username', flat=True))

    result = [[''] + usernames]

    commutes = Commute.objects.filter(date__gte=min, date__lte=max)
    commutes_by_username = groupby(commutes, key=lambda c: c.user.username)

    commutes_set = {}
    for username, group in commutes_by_username:
        commutes_set[username] = set(c.date for c in group)

    for single_date in daterange(datetime.strptime(min, '%Y-%m-%d'), datetime.strptime(max, '%Y-%m-%d')):
        row = [single_date]
        for username in usernames:
            try:
                if single_date in commutes_set[username]:
                    row.append('Y')
                else:
                    row.append('N')
            except KeyError:
                row.append('N')
        result.append(row)

    df = pd.DataFrame(result)
    pdf = SimpleDocTemplate(filename + '.pdf')
    table = Table(df.values.tolist())
    pdf.build([table])

    new_folder_path = "media/"

    os.rename(filename + '.pdf', os.path.join(new_folder_path, filename + '.pdf'))

    with open(os.path.join(new_folder_path, filename + '.pdf'), 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = \
            'attachment; filename=' + filename + '.pdf'
        return response
