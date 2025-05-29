from .models import Assignment, Feedback, STATUS_HISTORY, UploadRECIST

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from user.models import Contact
from .resources import AssignmentResource, FeedbackResource
from django.contrib import messages
from tablib import Dataset
from .utils import generate_search_query, compare_assignment_fields
from oncology_abc import utils
import json, collections


# Search request
def search(request):
    all_patient, query_dict = generate_search_query(request)
    search_count = all_patient.count()

    return render(request, 'pages/feedback/search.html', {'query': query_dict,
                                                          'search': all_patient,
                                                          'search_count': search_count})

# Feedback requests
@login_required()
def add_feedback(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    _feedback, errors = Feedback.feedback_form_validation(request, assignment)

    if errors:
        return JsonResponse({'code': 'error', 'error': errors})

    field_dict = dict(vars(_feedback))
    field_dict.pop('fu')
    new_feedback = Feedback(**field_dict)
    new_feedback.save()
    new_feedback.fu.set(_feedback.fu)

    if new_feedback.cycle == '1' and new_feedback.day == '1':
        assignment.status = 'ongoing'
        assignment.save()
    elif new_feedback.cycle == 'EOT' and new_feedback.fu.all().count() != 0:
        assignment.status = 'FU'
        assignment.save()
    elif new_feedback.eos is not None:
        assignment.status = 'off'
        assignment.save()

    return JsonResponse({'code': 'success'})


@login_required()
def edit_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, pk=feedback_id)
    edited_feedback, errors = Feedback.feedback_form_validation(request, None)

    if errors:
        return JsonResponse({'code': 'error', 'error': errors})

    feedback.cycle = edited_feedback.cycle
    feedback.day = edited_feedback.day
    feedback.tx_dose = edited_feedback.tx_dose
    feedback.toxicity = edited_feedback.toxicity
    feedback.dosing_date = edited_feedback.dosing_date
    feedback.eos = edited_feedback.eos
    feedback.next_visit = edited_feedback.next_visit
    feedback.photo_date = edited_feedback.photo_date
    feedback.response = edited_feedback.response
    feedback.response_text = edited_feedback.response_text
    feedback.comment = edited_feedback.comment
    feedback.scr_fail = edited_feedback.scr_fail
    feedback.ICF_date = edited_feedback.ICF_date
    feedback.uploader = edited_feedback.uploader
    feedback.is_accompany = edited_feedback.is_accompany
    feedback.fu.set(edited_feedback.fu)
    feedback.save()
    
    #if feedback.cycle == '1' and feedback.day == '1':
    #    feedback.assignment.status = 'ongoing'
    #    feedback.assignment.save()
    #elif feedback.cycle == 'EOT' and feedback.fu.all().count() != 0:
    #    feedback.assignment.status = 'FU'
    #    feedback.assignment.save()
    #elif feedback.eos is not None:
    #    feedback.assignment.status = 'off'
    #    feedback.assignment.save()

    return JsonResponse({'code': 'success'})


@login_required()
def delete_feedback(request, feedback_id):
    feedback = Feedback.objects.get(pk=feedback_id)
    assignment_id = feedback.assignment.id
    feedback.delete()
    return HttpResponseRedirect(f'/assignment/{assignment_id}/')


# Assignment requests
@login_required()
def detail_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    research = assignment.research
    backup = Contact.objects.filter(onco_A=1).order_by('name')
    if assignment.is_deleted:
        return render(request, 'pages/assignment/deleted.html', {
            'assignment': assignment
        })

    return render(request, 'pages/assignment/detail.html', {
        'assignment': assignment,
        'research': research,
        'assignment_field_choice': Assignment.field_value_and_text(),
        'feedback_field_choice': Feedback.field_value_and_text(),
        'feedbacks': assignment.feedback_set.prefetch_related('eos', 'fu').order_by('id'),
        'backup': backup,
        'upload_RECIST': UploadRECIST.objects.filter(is_deleted=False, assignment=assignment),
        'field_choice': Feedback.create_field_value_and_text(),
        'editable': True,
    })


@login_required()
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    backup = Contact.objects.filter(onco_A=1).order_by('name')
    research = assignment.research

    # GET req
    if request.method == 'GET':
        return render(
            request, 'pages/assignment/edit.html',
            {
             'assignment': assignment,
             'backup': backup,
             'research': research,
             'editable': True,
             'upload_RECIST': UploadRECIST.objects.filter(is_deleted=False, assignment=assignment),
             'assignment_field_choice': Assignment.field_value_and_text(),
             }
        )

    edited_assignment, errors = Assignment.assignment_form_validation(request, None)
    backup = Contact.objects.filter(onco_A=1).order_by('name')

    if errors:
        error_msg = {k: '<br>'.join(v) for k, v in errors.items()}
        edited_assignment.id = assignment.id
        return render(
            request, 'pages/assignment/edit.html',
            {
                'assignment': edited_assignment,
                'backup': backup,
                'research': research,
                'editable': True,
                'errors': error_msg,
                'assignment_field_choice': Assignment.field_value_and_text(),
                'upload_RECIST': UploadRECIST.objects.filter(is_deleted=False, assignment=assignment),
            }
        )

    prev_assignment_json = assignment.json()

    assignment.no = edited_assignment.no
    assignment.phase = edited_assignment.phase
    assignment.register_number = edited_assignment.register_number
    assignment.name = edited_assignment.name
    assignment.sex = edited_assignment.sex
    assignment.age = edited_assignment.age
    assignment.status = edited_assignment.status
    assignment.dx = edited_assignment.dx
    assignment.previous_tx = edited_assignment.previous_tx
    assignment.ECOG = edited_assignment.ECOG
    assignment.PI = edited_assignment.PI
    assignment.curr_crc = edited_assignment.curr_crc
    assignment.save()

    curr_assignment_json = assignment.json()
    field_summary = compare_assignment_fields(prev_assignment_json, curr_assignment_json)
    file_summary = collections.defaultdict(list)

    history = STATUS_HISTORY(user=request.user, assignment=assignment,
                             history_type=STATUS_HISTORY.EDIT_STATUS,
                             summary=json.dumps({
                                 'field_summary': field_summary
                             }),
                             content=assignment.json())
    history.save()

    if request.FILES.getlist('file[]'):
        prev_files = UploadRECIST.objects.filter(is_deleted=False, assignment=assignment)
        file_summary['prev'] = [f.json() for f in prev_files]
        prev_files.update(is_deleted=True)

    for _file in request.FILES.getlist('file[]'):
        new_file = UploadRECIST(filename=_file.name, file=_file, assignment=assignment)
        new_file.save()
        file_summary['curr'].append(new_file.json())

    return HttpResponseRedirect('/assignment/' + str(assignment.id) + '/')


@login_required()
def delete_assignment(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    research_id = assignment.research.id
    assignment.is_deleted = True
    assignment.save()
    return HttpResponseRedirect(f'/research/{research_id}/')


@login_required()
def assignment_upload(request):
    if request.method == 'POST':
        assignment_resource = AssignmentResource()
        dataset = Dataset()
        new_assignment = request.FILES['myfile']

        if not new_assignment.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'pages/assignment/upload.html')

        imported_data = dataset.load(new_assignment.read(), format='xlsx')
        for data in imported_data:
            value = Assignment(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6],
                data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15], data[16])
            value.save()

    return render(request, 'pages/assignment/upload.html')


@login_required()
def feedback_upload(request):
    if request.method == 'POST':
        feedback_resource = FeedbackResource()
        dataset = Dataset()
        new_feedback = request.FILES['myfile']

        if not new_feedback.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'pages/feedback/upload.html')

        imported_data = dataset.load(new_feedback.read(), format='xlsx')
        for data in imported_data:
            value = Feedback(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6],
                data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14], data[15])
            value.save()

    return render(request, 'pages/feedback/upload.html')
