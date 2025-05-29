import collections
import types
from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from user.models import Contact
from django.core.validators import MinValueValidator, MaxValueValidator
#from .forms import FormForm
#from .fields import ListTextWidget
#from django import forms
#from django.db.models import Count


RESPONSE_CHOICES = [
    ('', ''),
    ('CR', 'CR'),
    ('PR', 'PR'),
    ('SD', 'SD'),
    ('PD', 'PD'),
    ('ND', 'ND'),
]
RESPONSE_CHOICES_INV = {val: val for val, _ in RESPONSE_CHOICES}

DX_CHOICES = [
    ('stomach_cancer', 'Stomach cancer'),
    ('small_bowel_cancer', 'small bowel cancer'),
    ('colorectal_cancer', 'Colorectal cancer'),

    ('NSCLC', 'NSCLC'),
    ('SCLC', 'SCLC'),
    ('head_neck_cancer', 'Head/Neck cancer'),
    ('esophageal', 'esophageal'),

    ('hcc', 'HCC'),
    ('gb', 'GB'),
    ('BT', 'BT'),
    ('pancreatic_cancer', 'Pancreatic cancer'),

    ('breast_cancer', 'Breast cancer'),
    ('ovarian_cancer', 'Ovarian cancer'),
    ('endometrial_cancer', 'Endometrial cancer'),
    ('vaginal_cancer', 'Vaginal cancer'),
    ('cervix_cancer', 'Cervix cancer'),
    ('vulva_cancer', 'Vulva cancer'),

    ('rcc', 'RCC'),
    ('ureter_cancer', 'Ureter cancer'),
    ('bladder_cancer', 'Bladder cancer'),
    ('prostate_cancer', 'Prostate cancer'),

    ('solid_cancer', 'Solid cancer'),
    ('melanoma', 'Melanoma'),
    ('sarcoma', 'Sarcoma'),
    ('other', '기타(other)'),
]
DX_CHOICES_INV = {val: val for val, _ in DX_CHOICES}

STATUS_CHOICES = [
    ('screening', 'Screening'),
    ('screening_fail', 'Screening fail'),
    ('ongoing', 'On going'),
    ('off', 'Off'),
    ('FU', 'FU'),
    ('pre-screening', 'Pre-screening'),
    ('pre-screening-fail', 'Pre-screening fail'),
]
STATUS_CHOICES_INV = {val: val for val, _ in STATUS_CHOICES}

SEX_CHOICES = [
    ('M', 'M'),
    ('F', 'F'),
]
SEX_CHOICES_INV = {val: val for val, _ in SEX_CHOICES}

TRUE_OR_FALSE_CHOICES = [
    ('1', 'Y'),
    ('0', 'N'),
]
TRUE_OR_FALSE_CHOICES_INV = {val: val for val, _ in TRUE_OR_FALSE_CHOICES}


class FeedbackFieldModel(models.Model):
    class Meta:
        abstract = True

    CHOICES = tuple()
    INV_CHOICES = {}

    value = models.CharField(
        max_length=120,
        choices=CHOICES,
        null=True
    )

    @property
    def inv_choices(self):
        if not self.INV_CHOICES:
            self.INV_CHOICES = {value: text for value, text in self.CHOICES}
        return self.INV_CHOICES

    def json(self):
        return {
            'id': self.id,
            'type': self.value,
            'show': self.inv_choices[self.value]
        }

    def __str__(self):
        return self.inv_choices[self.value]


class EOS(FeedbackFieldModel):
    DEATH = 'death'
    WITHDRAWAL = 'withdrawal'
    COMPLETION = 'completion'
    ETC = 'etc'
    CHOICES = (
        (DEATH, '사망'),
        (WITHDRAWAL, '동의철회'),
        (COMPLETION, '완료'),
        (ETC, '기타'),
    )


class FU(FeedbackFieldModel):
    IMAGE = 'image'
    SURVIVAL = 'survival'
    CHOICES = (
        (IMAGE, '영상 f/u'),
        (SURVIVAL, '생존 f/u'),
    )


class Assignment(models.Model):
    # patient info
    phase = models.CharField(max_length=500, blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, blank=True, null=True)
    no = models.CharField(max_length=500, blank=True, null=True)
    register_number = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=500, blank=True, null=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    # attributes
    dx = models.CharField(choices=DX_CHOICES, max_length=500, blank=True, null=True)
    previous_tx = models.TextField(blank=True, null=True)
    ECOG = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
    # mata
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    # relations
    PI = models.CharField(max_length=100, blank=True, null=True)
    curr_crc = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    crc = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    research = models.ForeignKey('research.Research', on_delete=models.SET_NULL, null=True,
                                 blank=True)

    @staticmethod
    def field_value_and_text():
        ret = {
            'sex': SEX_CHOICES,
            'dx': DX_CHOICES,
            'status': STATUS_CHOICES,
        }
        return ret

    @staticmethod
    def assignment_form_validation(request, research):
        errors = collections.defaultdict(list)

        # Get field values
        no = request.POST.get('no')
        phase = request.POST.get('phase', '')
        register_number = request.POST.get('register_number')
        name = request.POST.get('name')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        status = request.POST.get('status')
        dx = request.POST.get('dx')
        previous_tx = request.POST.get('previous_tx')
        ECOG = request.POST.get('ECOG')
        PI = request.POST.get('PI')
        #curr_crc = request.POST.get('curr_crc')
        curr_crc_str = request.POST.get('curr_crc', '')
        if curr_crc_str != '':
            curr_crc = Contact.objects.get(id=int(curr_crc_str))
        if curr_crc_str == '':
            curr_crc = None

        # convert to proper values
        sex = SEX_CHOICES_INV.get(sex, None)
        age = None if not age else int(age)
        status = STATUS_CHOICES_INV.get(status, None)
        ECOG = None if not ECOG else int(ECOG)
        dx = DX_CHOICES_INV.get(dx, None)

        #if not no:
        #    errors['no'].append('- 연구 등록번호를 입력하세요.')
        if phase is None and research.id != 278:
            errors['phase'].append('- Phase를 선택하세요.')
        if not register_number:
            errors['register_number'].append('- 환자 등록번호를 입력하세요.')
        #if not name:
        #    errors['name'].append('- 이름을 입력하세요.')
        #if sex is None:
        #    errors['sex'].append('- 성별을 선택하세요.')
        #if age is None:
        #    errors['age'].append('- 나이를 입력하세요.')
        #if status is None:
        #    errors['status'].append('- Status를 선택하세요.')
        #if dx is None:
        #    errors['dx'].append('- DX를 선택하세요.')
        #if previous_Tx is None:
        #    errors['previous_Tx'].append('- previous Tx를 입력하세요.')
        #if PI is None:
        #    errors['PI'].append('- IP를 입력하세요.')
        #if not curr_crc:
        #    errors['curr_crc'].append('- 담당 CRC를 입력하세요.')
        #elif ' ' in curr_crc:
        #    errors['curr_crc'].append('- 공백(띄어쓰기)이 포함되어 있습니다.')
        if curr_crc_str == '':
            errors['curr_crc'].append('- 하나의 값은 선택되어야 합니다.')

        temp_assignment = types.SimpleNamespace()
        temp_assignment.no = no
        temp_assignment.phase = phase
        temp_assignment.register_number = register_number
        temp_assignment.name = name
        temp_assignment.sex = sex
        temp_assignment.age = age
        temp_assignment.status = status
        temp_assignment.dx = dx
        temp_assignment.previous_tx = previous_tx
        temp_assignment.ECOG = ECOG
        temp_assignment.PI = PI
        temp_assignment.curr_crc = curr_crc
        temp_assignment.research = research
        temp_assignment.crc = request.user

        return temp_assignment, errors

    def __str__(self):
        return f'({self.id}) {self.no} {self.register_number} {self.name} -> {self.research}'

    def json(self):
        assignment = {}
        assignment['no'] = self.no
        assignment['phase'] = self.phase
        assignment['register_number'] = self.register_number
        assignment['name'] = self.name
        assignment['sex'] = self.sex
        assignment['age'] = self.age
        assignment['status'] = self.status
        assignment['dx'] = self.dx
        assignment['previous_tx'] = self.previous_tx
        assignment['ECOG'] = self.ECOG
        assignment['PI'] = self.PI
        assignment['curr_crc'] = self.curr_crc

        assignment['file'] = [f.json() for f in self.uploadrecist_set.all()]
        assignment['history'] = [h.json() for h in
                               self.status_history_set.all().order_by('-create_date')]
        return assignment

def user_directory_path(instance, filename):
    return 'RECIST/assignment/{0}/{1}'.format(instance.assignment.id, filename)


class UploadRECIST(models.Model):
    is_deleted = models.BooleanField(default=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    filename = models.CharField(max_length=800)
    file = models.FileField(upload_to=user_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.file.url,
            'assignment': self.assignment.id,
            'filename': self.filename
        }


class Feedback(models.Model):
    # attributes
    scr_fail = models.DateField(blank=True, null=True)
    ICF_date = models.DateField(blank=True, null=True)
    cycle = models.CharField(max_length=500, default='', blank=True, null=True)
    day = models.CharField(max_length=500, default='', blank=True, null=True)
    dosing_date = models.DateField(blank=True, null=True)
    fu = models.ManyToManyField(FU)
    is_accompany = models.CharField(choices=TRUE_OR_FALSE_CHOICES, null=True, max_length=50, default='0')
    eos = models.ForeignKey(EOS, on_delete=models.SET_NULL, null=True)

    next_visit = models.DateField(blank=True, null=True)
    tx_dose = models.TextField(blank=True, null=True)
    photo_date = models.DateField(blank=True, null=True)
    response = models.CharField(choices=RESPONSE_CHOICES, max_length=500, default='', blank=True, null=True)
    response_text = models.CharField(max_length=500, default='', blank=True, null=True)
    #toxicity = FormForm
    toxicity = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    # meta
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # relations
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)


    @staticmethod
    def field_value_and_text():
        ret = {
            'response': RESPONSE_CHOICES,
        }
        return ret

    @staticmethod
    def create_field_value_and_text():
        m2m_field_list = [FU]
        ret = {}
        for c in m2m_field_list:
            c_lower_name = c.__name__.lower()
            choices = c.__dict__['CHOICES']
            ret[c_lower_name] = []
            for pk, choice in enumerate(choices):
                ret[c_lower_name].append(
                    [choice[0], choice[1]]
                )
        return ret

    @staticmethod
    def feedback_form_validation(request, assignment):
        errors = collections.defaultdict(list)

        # Get field values
        photo_date_str = request.POST.get('photo_date', '')
        response = request.POST.get('response', '')
        response_text = request.POST.get('response_text', '')
        toxicity = request.POST.get('toxicity', '')
        comment = request.POST.get('comment', '')
        scr_fail_str = request.POST.get('scr_fail', '')
        ICF_date_str = request.POST.get('ICF_date', '')
        cycle = request.POST.get('cycle', '')
        day = request.POST.get('day', '')
        dosing_date_str = request.POST.get('dosing_date', '')
        next_visit_str = request.POST.get('next_visit', '')
        tx_dose = request.POST.get('tx_dose', '')
        fu_types = request.POST.getlist('FU')
        fu = FU.objects.filter(value__in=fu_types)
        is_accompany = request.POST.get('is_accompany')
        is_accompany = TRUE_OR_FALSE_CHOICES_INV.get(is_accompany, None)
        eos_type = request.POST.get('eos')
        eos = EOS.objects.filter(value=eos_type).first()

        # convert to proper values
        response = RESPONSE_CHOICES_INV.get(response)

        try:
            photo_date = datetime.strptime(photo_date_str, '%m/%d/%Y')
        except:
            photo_date = None

        try:
            dosing_date = datetime.strptime(dosing_date_str, '%m/%d/%Y')
        except:
            dosing_date = None

        try:
            scr_fail = datetime.strptime(scr_fail_str, '%m/%d/%Y')
        except:
            scr_fail = None

        try:
            ICF_date = datetime.strptime(ICF_date_str, '%m/%d/%Y')
        except:
            ICF_date = None

        try:
            next_visit = datetime.strptime(next_visit_str, '%m/%d/%Y')
        except:
            next_visit = None
 
        if len(fu_types) > 0 and eos is not None:
            errors['FU'].append('- 한 가지 항목만 선택 가능합니다. (FU 항목은 중복 선택 가능)')
        if cycle == 'EOT' and len(fu_types) == 0 and eos is None:
            errors['FU'].append('- EOT 입력 시, FU or EOS 필수 선택입니다. FU 항목은 중복 선택 가능하며, EOS 항목은 하나의 값만 선택 가능합니다.')
        if cycle == '' and len(fu_types) != 0:
            errors['FU'].append('- EOT 입력 시, 선택 가능합니다.') 


        temp_feedback = types.SimpleNamespace()
        temp_feedback.photo_date = photo_date
        temp_feedback.dosing_date = dosing_date
        temp_feedback.fu = fu
        temp_feedback.is_accompany = is_accompany
        temp_feedback.eos = eos
        temp_feedback.next_visit = next_visit
        temp_feedback.response = response
        temp_feedback.response_text = response_text
        temp_feedback.toxicity = toxicity
        temp_feedback.comment = comment
        temp_feedback.scr_fail = scr_fail
        temp_feedback.ICF_date = ICF_date
        temp_feedback.cycle = cycle
        temp_feedback.day = day
        temp_feedback.tx_dose = tx_dose
        temp_feedback.assignment = assignment
        temp_feedback.uploader = request.user

        return temp_feedback, errors

    def __str__(self):
        return f'({self.id}) {self.assignment} {self.photo_date}'

    @property
    def get_html_url_next_visit(self):
        return f'<div class="next-visit-title"><a href="/assignment/{self.assignment.id}/" style="color:black;">' \
               f' {self.assignment.name} {self.assignment.register_number} {self.assignment.curr_crc}</a></div>'

    @property
    def get_html_url_drop(self):
        return f'<div class="next-visit-title"><a href="/assignment/{self.assignment.id}/" style="color:black; text-decoration:line-through;">' \
               f' {self.assignment.name} {self.assignment.register_number} </a></div>'

    @property
    def get_html_url_cycle(self):
        if not self.day:
            return f'<div class="cycle-title"><a href="/assignment/{self.assignment.id}/" style="color:black;"> ' \
                   f'{self.assignment.name} {self.assignment.register_number} {self.cycle} </a></div>'
        else:
            return f'<div class="cycle-title"><a href="/assignment/{self.assignment.id}/" style="color:black;"> ' \
                   f'{self.assignment.name} {self.assignment.register_number} C{self.cycle}D{self.day} </a></div>'


class STATUS_HISTORY(models.Model):
    EDIT_STATUS = 'edit_status'
    ADD_STATUS = 'add_status'
    CHOICES = (
        (ADD_STATUS, '상태 추가'),
        (EDIT_STATUS, '상태 수정')
    )
    INV_CHOICES = {value: text for value, text in CHOICES}

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.SET_NULL, null=True, blank=True)
    history_type = models.CharField(
        max_length=150,
        choices=CHOICES,
        null=False
    )
    summary = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def json(self):
        return {
            'id': self.id,
            'user': {
                'username': self.user.username,
            },
            'assignment': {
                'id': self.assignment.id,
                'name': self.assignment.name,
                'status': self.assignment.status,
            },
            'history_type': self.history_type,
            'summary': self.summary,
            'create_date': self.create_date
        }
