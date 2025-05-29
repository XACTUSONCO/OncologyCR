from django.views import generic
import io, xlsxwriter, locale, calendar, collections, itertools
from urllib.parse import quote
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models.functions import Cast, ExtractDay, ExtractMonth, ExtractYear, TruncDate, Coalesce
from django.db.models import CharField, Q, DateField, F, Func, Value, ExpressionWrapper, Sum, Count
from .utils import Calendar
import pandas as pd

from .models import Supporting, QC, Delivery, Research_Management
from research.models import Research
from feedback.models import Assignment, Feedback
from user.models import Contact
from leave.models import Patient

# Create your views here.
@login_required()
def download_vendor(request, research_id):
    research = get_object_or_404(Research, pk=research_id)
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # TODO Create total ongoing list header
    title_style = workbook.add_format({'border': 1, 'bottom': 2, 'align': 'center', 'bold': 1,'bg_color': '#BDBDBD', 'font_size': 13})
    border_center = workbook.add_format({'align': 'center', 'border': 1, 'bold': 1})
    vendor_cell = workbook.add_format({'top': 1, 'bottom': 1, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter'})

    # Create Vendor header
    vendor_header = [["CRO", 20],
                     ["Vendor Name", 20],
                     ["Information", 50],
                     ["Link", 35],
                     ["ID", 10],
                     ["PW", 10]]

    worksheet.merge_range('A1:E1', 'Vendor', title_style)
    research_management = Research_Management.objects.filter(is_deleted=False, research=research.id)

    row = 1
    col = 0
    for c_header, width in vendor_header:
        if c_header == 'CRO':
            for research_management in research_management:
                worksheet.merge_range(1, 0, 1, 4, 'CRO - ' + research_management.cro.value, border_center)
                row += 1
        else:
            worksheet.write(row, col, c_header, border_center)
        if c_header != 'CRO' and width is not None:
            worksheet.set_column(col, col, width)
            col += 1

    row += 1
    col = 0
    vendor = research_management.vendor.all()
    for i, vendor in enumerate(vendor):
        if i > 0:
            col = 0

        worksheet.write(row, col, vendor.value, vendor_cell)
        col += 1
        worksheet.write(row, col, vendor.information, vendor_cell)
        col += 1
        worksheet.write(row, col, vendor.link, vendor_cell)
        col += 1
        worksheet.write(row, col, vendor.vendor_id, vendor_cell)
        col += 1
        worksheet.write(row, col, vendor.vendor_pw, vendor_cell)

        row += 1

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    filename = research.research_name + ' - Vendor.xlsx'
    try:
        filename.encode('ascii')
        file_expr = 'filename="{}"'.format(filename)
    except UnicodeEncodeError:
        file_expr = "filename*=utf-8''{}".format(quote(filename))

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; ' + file_expr

    return response


@login_required()
@require_http_methods(['GET', 'POST'])
def edit_vendor(request, research_id):
    research = get_object_or_404(Research, pk=research_id)
    research_management = get_object_or_404(Research_Management, research=research.id)
    if request.method == 'GET':
        return render(request, 'pages/miscellaneous/vendor/edit.html',
                      {
                          'research': research,
                          'research_management': research_management,
                          'editable': True,
                          'field_choice': Research_Management.create_field_value_and_text(),
                      })
    temp_vendor, errors = Research_Management.vendor_form_validation(request, research)

    if errors:
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        temp_vendor.research.id = research.id
        return render(
            request, 'pages/miscellaneous/vendor/edit.html',
            {
                'research_management': temp_vendor,
                'editable': True,
                'errors': error_msg,
                'field_choice': Research_Management.create_field_value_and_text(),
            }
        )

    research_management.research = temp_vendor.research
    research_management.cro = temp_vendor.cro
    research_management.vendor.set(temp_vendor.vendor)
    research_management.save()

    return HttpResponseRedirect('/research/' + str(research.id) + '/')


@csrf_exempt
@login_required()
def supporting(request):
    today = datetime.today()
    this_sunday = today + timedelta(days=-today.weekday(), weeks=1) - timedelta(days=1)
    this_sunday_str = this_sunday.strftime('%Y/%m/%d')
    next_saturday = this_sunday + timedelta(days=6)
    next_saturday_str = next_saturday.strftime('%Y/%m/%d')
    next_supporting = Supporting.objects.filter(is_deleted='0', lab_date__gte=Cast(this_sunday, DateField()), lab_date__lte=next_saturday)\
                                        .order_by('lab_date__date', 'crc', 'assignment__name', 'lab_date__hour', 'lab_date__minute')\
                                        .values('id', 'lab_date', 'crc', 'supporting_type', 'comment', 'technician', 'kinds', 'post_hour',
                                                'create_date', 'assignment__research__research_name', 'assignment__register_number',
                                                'assignment__name', 'assignment__no', 'assignment__id')

    prev_sunday = this_sunday - timedelta(days=7)
    prev_sunday_str = prev_sunday.strftime('%Y/%m/%d')
    this_saturday = this_sunday - timedelta(days=1)
    this_saturday_str = this_saturday.strftime('%Y/%m/%d')
    this_supporting = Supporting.objects.filter(is_deleted='0', lab_date__gte=Cast(prev_sunday, DateField()), lab_date__lte=this_saturday) \
                                        .order_by('lab_date__date', 'crc', 'assignment__name', 'lab_date__hour', 'lab_date__minute')\
                                        .values('id', 'lab_date', 'crc', 'supporting_type', 'comment', 'technician', 'kinds', 'post_hour',
                                                'create_date', 'assignment__research__research_name', 'assignment__register_number',
                                                'assignment__name', 'assignment__no', 'assignment__id')

    assignments = Assignment.objects.filter(Q(is_deleted='0') & Q(curr_crc__user_id=request.user.id))\
                                    .order_by('research_id__research_name')\
                                    .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')
    technician_assignments = Assignment.objects.filter(Q(is_deleted='0'))\
                                               .order_by('research_id__research_name') \
                                               .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')
    technician = User.objects.filter(groups=5, is_active=1).values('first_name')

    option_radio = request.GET.get('optionRadios')
    if option_radio == 'period':
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')

        period_supporting = Supporting.objects.filter(Q(is_deleted='0', lab_date__gte=from_date,
                                                        lab_date__lte=datetime.strptime(request.GET.get('to_date'), '%Y-%m-%d') + timedelta(days=1))) \
                                        .order_by('lab_date__date', 'crc', 'assignment__name', 'lab_date__hour', 'lab_date__minute')\
                                        .values('id', 'lab_date', 'crc', 'supporting_type', 'comment', 'technician', 'kinds', 'post_hour',
                                                'create_date', 'assignment__research__research_name', 'assignment__register_number',
                                                'assignment__name', 'assignment__no', 'assignment__id')
        assignments = Assignment.objects.filter(Q(is_deleted='0') & Q(curr_crc__user_id=request.user.id))\
                                        .order_by('research_id__research_name') \
                                        .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')
        return render(request, 'pages/miscellaneous/supporting/supporting.html',
                      {'option_radio': option_radio, 'from_date': from_date, 'to_date': to_date, 'assignments': assignments, 'technician_assignments': technician_assignments, 'period_supporting': period_supporting})

    return render(request, 'pages/miscellaneous/supporting/supporting.html',
                  {'next_supporting': next_supporting, 'this_sun': this_sunday_str, 'next_sat': next_saturday_str,
                   'assignments': assignments, 'technician': technician, 'technician_assignments': technician_assignments,
                   'this_supporting': this_supporting, 'prev_sun': prev_sunday_str, 'this_sat': this_saturday_str,
                   'prev_sun_strp': prev_sunday, 'this_sat_strp': this_saturday, 'today': today,
                   'field_key_value': Supporting.create_field_value_and_text_dict(), 'editable': True})


@login_required()
@require_http_methods(['GET', 'POST'])
def add_supporting(request):
    if request.method == 'GET':
        parameter = request.GET.get('month')
        technician = request.GET.get('technician')
        assignments = Assignment.objects.filter(Q(is_deleted='0') & Q(curr_crc__user_id=request.user.id))\
                                        .order_by('research_id__research_name') \
                                        .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')
        technician_assignments = Assignment.objects.filter(Q(is_deleted='0'))\
                                                   .order_by('research_id__research_name')\
                                                   .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')
        return render(request, 'pages/miscellaneous/supporting/add.html',
                           {'assignments': assignments, 'technician_assignments': technician_assignments, 'parameter': parameter, 'technician': technician, 'editable': True,})

    temp_supporting, errors = Supporting.supporting_form_validation(request)

    if errors:
        parameter = request.GET.get('month')
        technician = request.GET.get('technician')
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        assignments = Assignment.objects.filter(Q(is_deleted='0') & Q(curr_crc__user_id=request.user.id)) \
            .order_by('research_id__research_name') \
            .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')
        technician_assignments = Assignment.objects.filter(Q(is_deleted='0')) \
            .order_by('research_id__research_name') \
            .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')
        return render(request, 'pages/miscellaneous/supporting/add.html',
            {
            'parameter': parameter,
            'technician': technician,
            'assignments': assignments,
            'technician_assignments': technician_assignments,
            'supporting': temp_supporting,
            'editable': True,
            'errors': error_msg,
            }
        )

    # Create new Supporting request
    supporting = Supporting(**dict(vars(temp_supporting)))
    supporting.save()
    return HttpResponseRedirect('/miscellaneous/supporting/')

    #if request.method == 'GET':
    #    formset = SupportingModelFormset(queryset=Supporting.objects.none())
    #elif request.method == 'POST':
    #    formset = SupportingModelFormset(request.POST, form_kwargs={'crc': request.user.first_name})
    #    if formset.is_valid():
    #        for form in formset:
    #            form.save()
    #        return redirect('miscellaneous:supporting_list')
    #return render(request, 'pages/miscellaneous/supporting/add.html', {'formset': formset})


@login_required()
def add_new_supporting(request, id):
    if request.method == 'GET':
        supporting = Supporting.objects.filter(pk=id)[0]
        return render(request, 'pages/miscellaneous/supporting/add_new.html', {'supporting': supporting, 'editable': True})

    temp_supporting, errors = Supporting.supporting_form_validation(request)

    if errors:
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        return render(
            request, 'pages/miscellaneous/supporting/add_new.html',
            {
                'supporting': temp_supporting,
                'editable': True,
                'errors': error_msg
            }
        )

    # Create new Supporting request
    supporting = Supporting(**dict(vars(temp_supporting)))
    supporting.save()
    return HttpResponseRedirect('/miscellaneous/supporting/')


@login_required()
def edit_supporting(request, id):
    supporting = get_object_or_404(Supporting, pk=id)
    assignments = Assignment.objects.filter(Q(is_deleted='0') & Q(curr_crc__user_id=request.user.id)) \
        .order_by('research_id__research_name') \
        .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')
    technician_assignments = Assignment.objects.filter(Q(is_deleted='0')) \
        .order_by('research_id__research_name') \
        .values('id', 'no', 'register_number', 'name', 'research__research_name', 'status')

    # GET req
    if request.method == 'GET':
        return render(
            request, 'pages/miscellaneous/supporting/edit.html',
            {
             'supporting': supporting,
             'assignments': assignments,
             'technician_assignments': technician_assignments,
             'editable': True,
             #'field_choice': Research.create_field_value_and_text(),
             #'field_key_value': Research.create_field_value_and_text_dict(),
             }
        )

    temp_supporting, errors = Supporting.supporting_form_validation(request)

    if errors:
        # Temporary set attributes. cf. It is not a model instance!
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        temp_supporting.id = supporting.id
        return render(
            request, 'pages/miscellaneous/supporting/edit.html',
            {
                'supporting': temp_supporting,
                'assignments': assignments,
                'technician_assignments': technician_assignments,
                'editable': True,
                #'field_choice': Research.create_field_value_and_text(),
                #'field_key_value': Research.create_field_value_and_text_dict(),
                'errors': error_msg,
            }
        )

    supporting.lab_date = temp_supporting.lab_date
    supporting.assignment = temp_supporting.assignment
    supporting.kinds = temp_supporting.kinds
    supporting.post_hour = temp_supporting.post_hour
    supporting.crc = temp_supporting.crc
    supporting.comment = temp_supporting.comment
    supporting.technician = temp_supporting.technician
    supporting.supporting_type = temp_supporting.supporting_type
    supporting.save()

    return HttpResponseRedirect('/miscellaneous/supporting/')


@login_required()
def delete_supporting(request, id):
    supporting = Supporting.objects.get(pk=id)
    supporting.is_deleted = True
    supporting.save()
    return HttpResponseRedirect(f'/miscellaneous/supporting/')

@login_required()
def download_supporting(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    merge_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    today = datetime.today()
    this_sunday = today + timedelta(days=-today.weekday(), weeks=1) - timedelta(days=1)
    this_sunday_str = this_sunday.strftime('%Y/%m/%d')
    next_saturday = this_sunday + timedelta(days=6)
    next_saturday_str = next_saturday.strftime('%Y/%m/%d')
    supportings = Supporting.objects.filter(is_deleted='0', lab_date__gte=this_sunday, lab_date__lte=next_saturday).order_by('lab_date') \
        .annotate(lab_date_str=Cast(TruncDate('lab_date'), CharField())) \
        .values_list('lab_date_str', 'lab_date_str', 'assignment__research__research_name',
                     'assignment__register_number', 'assignment__name', 'assignment__no', 'lab_date_str', 'kinds', 'crc', 'comment', 'technician')

    supportings = pd.DataFrame.from_records(supportings)
    supportings = supportings.rename(columns={0: '요일',
                                              1: 'Date',
                                              2: 'Research name',
                                              3: 'Register Number',
                                              4: 'Name',
                                              5: 'No',
                                              6: 'Time',
                                              7: 'Kinds',
                                              8: 'CRC',
                                              9: 'Comment',
                                              10: 'Technician'})

    for supporting in supportings['요일'].unique():
        # find indices and add one to account for header
        u = supportings.loc[supportings['요일'] == supporting].index.values + 1

        if len(u) < 2:
            pass  # do not merge cells if there is only one supporting 요일
        else:
            # merge cells using the first and last indices
            worksheet.merge_range(u[0], 0, u[-1], 0, supportings.loc[u[0], '요일'], merge_format)


    workbook.close()
    output.seek(0)

    supportings.set_index(supportings.columns[:-1].tolist()).to_excel('success.xlsx')

    filename = 'Blood Sample List (' + this_sunday_str + '~' + next_saturday_str + ').xlsx'
    try:
        filename.encode('ascii')
        file_expr = 'filename="{}"'.format(filename)
    except UnicodeEncodeError:
        file_expr = "filename*=utf-8''{}".format(quote(filename))

    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; ' + file_expr

    return response


@csrf_exempt
@login_required()
def delete_technician(request):
    if request.method == 'POST':
        supporting_ids = request.POST.getlist('chkArray[]')
        supportings = Supporting.objects.filter(id__in=supporting_ids).values_list('id', flat=True)
        for supporting in supportings:
            supporting = Supporting.objects.get(pk=supporting)
            supporting.technician = ''
            supporting.save()
    return render(request, 'pages/miscellaneous/supporting/supporting.html')

@csrf_exempt
@login_required()
def update_technician(request):
    if request.method == 'POST':
        supporting_ids = request.POST.getlist('chkArray[]')
        supportings = Supporting.objects.filter(id__in=supporting_ids).values_list('id', flat=True)
        for supporting in supportings:
            supporting = Supporting.objects.get(pk=supporting)
            if supporting.technician != '':
                supporting.technician = supporting.technician
            else:
                supporting.technician = request.user.first_name
            supporting.save()
    return render(request, 'pages/miscellaneous/supporting/supporting.html')


class CalendarView(generic.ListView):
    model = Patient
    template_name = 'pages/miscellaneous/this_week_patient_list/this_week_patient_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)
        cal.setfirstweekday(6)

        #Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)

        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

@login_required()
def download_this_week_patient_list(request):
    next_mon = datetime.today() + timedelta(days=-datetime.today().weekday(), weeks=1)
    next_fri = next_mon + timedelta(days=5)
    #next_mon = datetime(2024,7,1) 
    #next_fri = datetime(2024,7,5)

    this_week_patient_list = Feedback.objects.filter(assignment__is_deleted=0, next_visit__isnull=False, next_visit__gte=next_mon, next_visit__lte=next_fri) \
                                .values('next_visit', 'assignment_id__research_id__research_name', 'assignment__curr_crc__name',
                                        'assignment__name','assignment__register_number')\
                                .order_by('next_visit', 'assignment_id__research_id__research_name')

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('전체임상환자명단')
    worksheet2 = workbook.add_worksheet('종양내과 A팀 Clinical Research')

    # TODO Create total ongoing list header
    title = workbook.add_format({'border': 1, 'bottom': 2, 'align': 'center', 'bold': 1,'bg_color': '#BDBDBD', 'font_size': 13})
    border_center = workbook.add_format({'align': 'center', 'border': 1, 'bold': 1})
    this_week_patient_list_start = workbook.add_format({'top': 1, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter'})
    this_week_patient_list_end = workbook.add_format({'bottom': 1, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter'})
    ongoing_research_list_textwrap = workbook.add_format({'bottom': 1, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter', 'text_wrap': True})

    # Create Assignment header
    this_week_patient_list_header = [["날짜", 15],
                                      ["연구명", 25],
                                      ["환자/등록번호", 25],
                                      ["담당 CRC (연락처)", 30]]

    title_style = title
    worksheet.merge_range('A1:D1', '전체임상환자명단', title_style)

    row = 1
    col = 0
    for a_header, width in this_week_patient_list_header:
        worksheet.write(row, col, a_header, border_center)
        if width is not None:
            worksheet.set_column(col, col, width)
        col += 1

        for i, patient in enumerate(this_week_patient_list):
            if i == 0:
                style = this_week_patient_list_start
            elif i == len(this_week_patient_list) - 1:
                style = this_week_patient_list_end

    row += 1
    col = 0
    for patient in this_week_patient_list:
        worksheet.write(row, col, datetime.strftime(patient['next_visit'], '%Y-%m-%d'), style)
        col += 1
        worksheet.write(row, col, patient['assignment_id__research_id__research_name'], style)
        col += 1
        worksheet.write(row, col, patient['assignment__name'] + ' / ' +patient['assignment__register_number'], style)
        col += 1
        contact = Contact.objects.filter(onco_A=1, name=patient['assignment__curr_crc__name']).values('phone', 'work_phone')
        worksheet.write(row, col, patient['assignment__curr_crc__name'] + ' (' +  contact[0]['phone'] + ', ' + contact[0]['work_phone'] + ')', style)
        col += 1

        row += 1
        col = 0

    # 종양내과 A팀 Clinical Research
    ongoing_research_list = Research.objects.filter(Q(is_deleted=0, onco_A=1)).values('crc__name', 'research_name', 'contact').order_by('crc__name')
    ongoing_research_header = [["담당 CRC (연락처)", 30], ["연구명", 30]]
    worksheet2.merge_range('A1:B1', '종양내과 A팀 Clinical Research', title_style)

    row = 1
    col = 0
    for b_header, width in ongoing_research_header:
        worksheet2.write(row, col, b_header, border_center)
        if width is not None:
            worksheet2.set_column(col, col, width)
        col += 1

        for i, patient in enumerate(ongoing_research_list):
            if i == 0:
                style = this_week_patient_list_start
            elif i == len(ongoing_research_list) - 1:
                style = this_week_patient_list_end

    row += 1
    col = 0
    for ongoing_research in ongoing_research_list:
        worksheet2.write(row, col, str(ongoing_research['crc__name']) + '\n' + ' (' + ongoing_research['contact'] + ')', ongoing_research_list_textwrap)
        col += 1
        worksheet2.write(row, col, ongoing_research['research_name'], style)
        col += 1

        row += 1
        col = 0

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    filename = '전체임상환자명단 ' + datetime.strftime(next_mon, '%y%m%d') + '.xlsx'
    try:
        filename.encode('ascii')
        file_expr = 'filename="{}"'.format(filename)
    except UnicodeEncodeError:
        file_expr = "filename*=utf-8''{}".format(quote(filename))

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; ' + file_expr

    return response


@login_required()
@require_http_methods(['GET', 'POST'])
def add_delivery(request):
    if request.method == 'GET':
        delivery_assignments = Assignment.objects.filter(is_deleted='0', research_id=94).order_by('create_date')
        return render(request, 'pages/miscellaneous/94/add.html',
                           {'delivery_assignments': delivery_assignments, 'editable': True})

    temp_delivery, errors = Delivery.delivery_form_validation(request)

    if errors:
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        delivery_assignments = Assignment.objects.filter(is_deleted='0', research_id=94).order_by('create_date')
        return render(request, 'pages/miscellaneous/94/add.html',
            {
            'delivery_assignments': delivery_assignments,
            'delivery': temp_delivery,
            'editable': True,
            'errors': error_msg,
            }
        )

    delivery = Delivery(**dict(vars(temp_delivery)))
    delivery.save()
    return HttpResponseRedirect('/research/94/')

@login_required()
def edit_delivery(request, id):
    delivery = get_object_or_404(Delivery, pk=id)
    edited_delivery, errors = Delivery.delivery_form_validation(request)

    if errors:
        return JsonResponse({'code': 'error', 'error': errors})

    delivery.visit_date = edited_delivery.visit_date
    delivery.assignment = edited_delivery.assignment
    delivery.crc = edited_delivery.crc
    delivery.scheduled_time = edited_delivery.scheduled_time
    delivery.comment = edited_delivery.comment
    delivery.save()
    return JsonResponse({'code': 'success'})

@login_required()
def delete_delivery(request, id):
    delivery = Delivery.objects.get(pk=id)
    delivery.is_deleted = True
    delivery.save()
    return HttpResponseRedirect(f'/research/94/')

@csrf_exempt
@login_required()
def delete_checked(request):
    if request.method == 'POST':
        delivery_ids = request.POST.getlist('chkArray[]')
        deliveries = Delivery.objects.filter(id__in=delivery_ids).values_list('id', flat=True)
        for delivery in deliveries:
            delivery = Delivery.objects.get(pk=delivery)
            delivery.checking = ''
            delivery.save()
    return HttpResponseRedirect(f'/research/94/')

@csrf_exempt
@login_required()
def update_checked(request):
    if request.method == 'POST':
        delivery_ids = request.POST.getlist('chkArray[]')
        deliveries = Delivery.objects.filter(id__in=delivery_ids).values_list('id', flat=True)
        for delivery in deliveries:
            delivery = Delivery.objects.get(pk=delivery)
            delivery.checking = 'O'
            delivery.save()
    return HttpResponseRedirect(f'/research/94/')

@login_required
def download_IV_delivery(request):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    this_monday = date.today() - timedelta(days=date.today().weekday())
    this_monday_str = this_monday.strftime('%y%m%d')
    this_sunday = this_monday + timedelta(days=6)
    this_sunday_str = this_sunday.strftime('%y%m%d')

    # TODO Create total ongoing list header
    title_style = workbook.add_format({'border': 1, 'bottom': 2, 'align': 'center', 'bold': 1,'bg_color': '#BDBDBD', 'font_size': 13})
    border_center = workbook.add_format({'align': 'center', 'border': 1, 'bold': 1})
    delivery_cell = workbook.add_format({'top': 1, 'bottom': 1, 'left': 1, 'right': 1, 'align': 'center', 'valign': 'vcenter'})

    # Create Vendor header
    delivery_header = [["요일", 5],
                       ["날짜", 10],
                       ["등록번호", 10],
                       ["이름", 7],
                       ["담당 CRC", 10],
                       ["시행 예정 시간", 15],
                       ["Comment", 40]]

    worksheet.merge_range('A1:G1', 'ALBATROSS - IV(Naseron) Delivery 명단 ' + this_monday_str + '~' + this_sunday_str, title_style)

    row = 1
    col = 0
    for d_header, width in delivery_header:
        worksheet.write(row, col, d_header, border_center)
        if width is not None:
            worksheet.set_column(col, col, width)
        col += 1

        #for i, patient in enumerate(this_week_patient_list):
        #    if i == 0:
        #        style = this_week_patient_list_start
        #    elif i == len(this_week_patient_list) - 1:
        #        style = this_week_patient_list_end

    row += 1
    col = 0
    delivery = Delivery.objects.filter(is_deleted=0, visit_date__gte=this_monday, visit_date__lte=this_sunday)
    for i, delivery in enumerate(delivery):
        if i > 0:
            col = 0
        locale.setlocale(locale.LC_ALL, 'ko_KR.UTF-8')
        worksheet.write(row, col, datetime.strftime(delivery.visit_date, '%a'), delivery_cell)
        col += 1
        worksheet.write(row, col, datetime.strftime(delivery.visit_date, '%Y-%m-%d'), delivery_cell)
        col += 1
        worksheet.write(row, col, delivery.assignment.register_number, delivery_cell)
        col += 1
        worksheet.write(row, col, delivery.assignment.name, delivery_cell)
        col += 1
        worksheet.write(row, col, delivery.crc, delivery_cell)
        col += 1
        worksheet.write(row, col, delivery.scheduled_time, delivery_cell)
        col += 1
        worksheet.write(row, col, delivery.comment, delivery_cell)

        row += 1

    # Close the workbook before sending the data.
    workbook.close()

    # Rewind the buffer.
    output.seek(0)

    filename = 'ALBATROSS - IV(Naseron) Delivery 명단 ' + this_monday_str + '-' + this_sunday_str + '.xlsx'
    try:
        filename.encode('ascii')
        file_expr = 'filename="{}"'.format(filename)
    except UnicodeEncodeError:
        file_expr = "filename*=utf-8''{}".format(quote(filename))

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; ' + file_expr

    return response

@csrf_exempt
@login_required()
def delete_objects(request):
    if request.method == 'POST':
        supporting_ids = request.POST.getlist('chkArray[]')
        supportings = Supporting.objects.filter(id__in=supporting_ids).values_list('id', flat=True)
        for supporting in supportings:
            supporting = Supporting.objects.get(pk=supporting)
            supporting.is_deleted = 1
            supporting.save()
    return render(request, 'pages/miscellaneous/supporting/supporting.html')


@login_required()
def QC_index(request):
    today = datetime.today()
    if today.month == 1:
        first_day = datetime(today.year-1, 12, 1)
    elif today.month != 1:
        first_day = datetime(today.year, today.month - 1, 1)
    last_day = datetime(today.year, today.month, 1) - timedelta(days=1)
    QC_by_research = QC.objects.filter(is_deleted=0, start=first_day, end=last_day) \
                         .values('vendor__value', 'QC_category', 'research__research_name') \
                         .annotate(QcCount=Coalesce(Sum('QC_count', dinstinct=True), 0)) \
                         .order_by('vendor__value', 'research__research_name')

    QC_by_crc = QC.objects.filter(is_deleted=0, start=first_day, end=last_day) \
                        .values('vendor__value', 'research__crc__name', 'QC_category') \
                        .annotate(QcCount=Coalesce(Sum('QC_count', dinstinct=True), 0)) \
                        .order_by('vendor__value')

    QC_by_PI = QC.objects.filter(is_deleted=0, start=first_day, end=last_day) \
                        .values('vendor__value', 'research__PI', 'research__research_name') \
                        .annotate(QcCount=Coalesce(Sum('QC_count', dinstinct=True), 0)) \
                        .order_by('vendor__value', 'research__research_name')

    annotations = {}
    types = ('AE', 'RECIST', 'LAB', 'DOSAGE', 'ERROR_ETC', 'OMISSION_ETC', 'CYCLE', 'TOTAL')

    for i, type in enumerate(types):
        if type != 'TOTAL':
            annotations[f'{type}'] = Coalesce(Sum('QC_count', filter=Q(QC_category=i+1), dinstinct=True), 0)
        elif type == 'TOTAL':
            annotations['TOTAL'] = Coalesce(Sum('QC_count', dinstinct=True), 0)

        # Vendor에 따른 연구별 쿼리 종류 및 개수
        query_by_research = QC.objects.filter(is_deleted=0, start=first_day, end=last_day)\
                                      .values('research').distinct().order_by('research__research_name')\
                                      .annotate(**annotations).values('research__research_name', *annotations.keys())

        # Vendor에 따른 CRC별 쿼리 종류 및 개수
        query_by_CRC = QC.objects.filter(is_deleted=0, start=first_day, end=last_day)\
                                      .values('crc').distinct().order_by('crc__name')\
                                      .annotate(**annotations).values('crc__name', *annotations.keys())

        # Vendor에 따른 PI별 쿼리 종류 및 개수
        query_by_PI = QC.objects.filter(is_deleted=0, start=first_day, end=last_day) \
                .values('research__PI').distinct().order_by('research__PI') \
                .annotate(**annotations).values('research__PI', *annotations.keys())

    query_by_research_dict = collections.defaultdict(list)
    for type_, query in itertools.product(types, query_by_research):
        query_by_research_dict[f'{type_}'].append(str(query[f'{type_}']))
    research_list = [];
    for research in query_by_research:
        research_list.append(str(research['research__research_name']))

    query_by_CRC_dict = collections.defaultdict(list)
    for type_, query in itertools.product(types, query_by_CRC.values('crc__name', *annotations.keys())):
        query_by_CRC_dict[f'{type_}'].append(str(query[f'{type_}']))
    CRC_list = [];
    for CRC in query_by_CRC:
        CRC_list.append(str(CRC['crc__name']))

    query_by_PI_dict = collections.defaultdict(list)
    for type_, query in itertools.product(types, query_by_PI.values('research__PI', *annotations.keys())):
        query_by_PI_dict[f'{type_}'].append(str(query[f'{type_}']))
    PI_list = [];
    for PI in query_by_PI:
        PI_list.append(str(PI['research__PI']))

    if request.GET.get('from_date'):
        option_radio = request.GET.get('optionRadios')
        period_from_date = request.GET.get('from_date')
        period_to_date = request.GET.get('to_date')
        QC_index = QC.objects.filter(Q(is_deleted=0) & (Q(start=period_from_date) | Q(end=period_to_date))) \
                             .select_related('vendor', 'research', 'QC_category')

        annotations = {}
        types = ('AE', 'RECIST', 'LAB', 'DOSAGE', 'ERROR_ETC', 'OMISSION_ETC', 'CYCLE', 'TOTAL')

        for i, type in enumerate(types):
            if type != 'TOTAL':
                annotations[f'{type}'] = Coalesce(Sum('QC_count', filter=Q(QC_category=i + 1), dinstinct=True), 0)
            elif type == 'TOTAL':
                annotations['TOTAL'] = Coalesce(Sum('QC_count', dinstinct=True), 0)

            # Vendor에 따른 연구별 쿼리 종류 및 개수
            query_by_research = QC.objects.filter(Q(is_deleted=0) & (Q(start=period_from_date) | Q(end=period_to_date))) \
                .values('research').distinct().order_by('research__research_name') \
                .annotate(**annotations).values('research__research_name', *annotations.keys())

            # Vendor에 따른 CRC별 쿼리 종류 및 개수
            query_by_CRC = QC.objects.filter(Q(is_deleted=0) & (Q(start=period_from_date) | Q(end=period_to_date))) \
                .values('crc').distinct().order_by('crc__name') \
                .annotate(**annotations).values('crc__name', *annotations.keys())

            # Vendor에 따른 PI별 쿼리 종류 및 개수
            query_by_PI = QC.objects.filter(Q(is_deleted=0) & (Q(start=period_from_date) | Q(end=period_to_date))) \
                .values('research__PI').distinct().order_by('research__PI') \
                .annotate(**annotations).values('research__PI', *annotations.keys())

        query_by_research_dict = collections.defaultdict(list)
        for type_, query in itertools.product(types, query_by_research):
            query_by_research_dict[f'{type_}'].append(str(query[f'{type_}']))

        research_list = [];
        for research in query_by_research:
            research_list.append(str(research['research__research_name']))

        query_by_CRC_dict = collections.defaultdict(list)
        for type_, query in itertools.product(types, query_by_CRC):
            query_by_CRC_dict[f'{type_}'].append(str(query[f'{type_}']))
        CRC_list = [];
        for CRC in query_by_CRC:
            CRC_list.append(str(CRC['crc__name']))

        query_by_PI_dict = collections.defaultdict(list)
        for type_, query in itertools.product(types, query_by_PI):
            query_by_PI_dict[f'{type_}'].append(str(query[f'{type_}']))
        PI_list = [];
        for PI in query_by_PI:
            PI_list.append(str(PI['research__PI']))

        return render(request, 'pages/miscellaneous/QC/QC.html', {'QC': QC_index,
                                                                  'option_radio': option_radio, 'from_date': period_from_date, 'to_date': period_to_date,
                                                                  'research_list': research_list, 'query_by_research': query_by_research, 'query_by_research_dict': query_by_research_dict,
                                                                  'CRC_list': CRC_list, 'query_by_CRC': query_by_CRC, 'query_by_CRC_dict': query_by_CRC_dict,
                                                                  'PI_list': PI_list, 'query_by_PI': query_by_PI, 'query_by_PI_dict': query_by_PI_dict})

    return render(request, 'pages/miscellaneous/QC/QC.html', {'QC_by_research': QC_by_research, 'QC_by_crc': QC_by_crc, 'QC_by_PI': QC_by_PI, 'first_day': first_day, 'last_day': last_day,
                                                              'research_list': research_list, 'query_by_research': query_by_research, 'query_by_research_dict': query_by_research_dict,
                                                              'CRC_list': CRC_list, 'query_by_CRC': query_by_CRC, 'query_by_CRC_dict': query_by_CRC_dict,
                                                              'PI_list': PI_list, 'query_by_PI': query_by_PI, 'query_by_PI_dict': query_by_PI_dict})


@login_required()
@require_http_methods(['GET', 'POST'])
def add_QC(request):
    if request.method == 'GET':
        new_QC = QC()
        research = Research.objects.filter(is_deleted='0').order_by('research_name').values('research_name', 'id')
        crc = Contact.objects.filter(onco_A=1).order_by('name')
        return render(
            request, 'pages/miscellaneous/QC/add.html', {
                'QC': new_QC,
                'research': research,
                'crc': crc,
                'field_choice': QC.create_field_value_and_text_dict(),
                'editable': True})

    temp_QC, errors = QC.QC_form_validation(request)

    if errors:
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        research = Research.objects.filter(is_deleted='0').order_by('research_name').values('research_name', 'id')
        crc = Contact.objects.filter(onco_A=1).order_by('name')
        return render(
            request, 'pages/miscellaneous/QC/add.html',
            {
                'QC': temp_QC,
                'research': research,
                'crc': crc,
                'editable': True,
                'field_choice': QC.create_field_value_and_text_dict(),
                'errors': error_msg,
            }
        )

    field_dict = dict(vars(temp_QC))
    new_QC = QC(**field_dict)
    new_QC.save()

    return HttpResponseRedirect('/miscellaneous/QC')

@login_required()
def edit_QC(request, id):
    qc = get_object_or_404(QC, pk=id)
    crc = Contact.objects.filter(Q(onco_A=1) & ~Q(team__name='etc')).order_by('name')
    research = Research.objects.filter(is_deleted='0').order_by('research_name').values('research_name', 'id')
    # GET req
    if request.method == 'GET':
        return render(
            request, 'pages/miscellaneous/QC/edit.html',
            {
             'crc': crc,
             'QC': qc,
             'research': research,
             'field_choice': QC.create_field_value_and_text_dict(),
             'editable': True,
             }
        )

    temp_QC, errors = QC.QC_form_validation(request)
    crc = Contact.objects.filter(Q(onco_A=1) & ~Q(team__name='etc')).order_by('name')

    if errors:
        # Temporary set attributes. cf. It is not a model instance!
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        temp_QC.id = QC.id
        return render(
            request, 'pages/miscellaneous/QC/edit.html',
            {
                'crc': crc,
                'QC': temp_QC,
                'research': research,
                'field_choice': QC.create_field_value_and_text_dict(),
                'editable': True,
                'errors': error_msg,
            }
        )

    qc.vendor = temp_QC.vendor
    qc.research = temp_QC.research
    qc.crc = temp_QC.crc
    qc.QC_category = temp_QC.QC_category
    qc.QC_count = temp_QC.QC_count
    qc.start = temp_QC.start
    qc.end = temp_QC.end
    qc.save()

    return HttpResponseRedirect('/miscellaneous/QC/')

@login_required()
def delete_QC(request, id):
    qc = QC.objects.get(pk=id)
    qc.is_deleted = True
    qc.save()
    return HttpResponseRedirect(f'/miscellaneous/QC/')
