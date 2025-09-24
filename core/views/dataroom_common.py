from research.models import Research, UploadFile, UploadEngFile, UploadInclusion, UploadExclusion, UploadReference
from dataroom.models import protocol_upload
from django.db.models import Q
from django.shortcuts import render


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