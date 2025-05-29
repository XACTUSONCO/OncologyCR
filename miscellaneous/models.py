from django.db import models
from research.models import Research
from feedback.models import Assignment
from user.models import Contact
import collections, types
from datetime import datetime

KINDS_CHOICES = [
    ('PK-pre', 'PK-pre'),
    ('PK-post', 'PK-post'),
    ('EKG', 'EKG'),
    ('PK/EKG', 'PK/EKG'),
    ('Bx', 'Bx'),
    ('LAB', 'LAB'),
    ('PK+LAB', 'PK+LAB'),
]
KINDS_CHOICES_INV = {val: val for val, _ in KINDS_CHOICES}

SUPPORTING_TYPE_CHOICES = [
    ('진검검체', '진검검체'),
    ('별도채혈', '별도채혈'),
    ('채혈실동행', '채혈실동행'),
    ('분주', '분주'),
]
SUPPORTING_TYPE_CHOICES_INV = {val: val for val, _ in SUPPORTING_TYPE_CHOICES}

TIME_CHOICES = [
    ('오전', '오전'),
    ('오후', '오후'),
    ('기타', '기타'),
]
TIME_CHOICES_INV = {val: val for val, _ in TIME_CHOICES}

# Create your models here.
class ResearchFieldModel(models.Model):
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


class CRO(ResearchFieldModel):
    ADM_Korea_CRO = 'ADM Korea'
    AllLive_Healthcare_CRO = 'AllLive Healthcare'
    BDM_Consulting_CRO = 'BDM Consulting'
    BETHESDASOFT_CRO = 'BETHESDASOFT'
    C_R_Research_CRO = 'C&R Research'
    CALEB_MULTILAB_CRO = 'CALEB MULTILAB'
    CC_I_Research_CRO = 'CC&I Research'
    CiKLux_CRO = 'CiKLux'
    Clinical_CRO_CRO = 'Clinical CRO'
    CliPS_CRO = 'CliPS'
    D2S_CRO = 'D2S'
    HELPTRIAL_CRO = 'HELPTRIAL'
    ICON_CRO = 'ICON'
    IQVIA_CRO = 'IQVIA'
    JNPMEDI_CRO = 'JNPMEDI'
    KCSG_CRO = 'KCSG'
    KHMEDICARE_CRO = 'KHMEDICARE'
    Kolab_CRO = 'Kolab'
    LSK_Global_PS_CRO = 'LSK Global PS'
    Medi_Help_Line_CRO = 'Medi Help Line'
    Medical_Excellence_CRO = 'Medical Excellence'
    Medical_Writing_CRO = 'Medical Writing'
    PAREXEL_CRO = 'PAREXEL'
    PHARMACRO_CRO = 'PHARMACRO'
    PLS_CRO = 'PLS'
    PROMEDIS_CRO = 'PROMEDIS'
    Research_Mentor_CRO = 'Research Mentor'
    RNDMotiv_CRO = 'RNDMotiv'
    SEO_CHO_CRO_CRO = 'SEO-CHO CRO'
    SEOUL_CRO_CRO = 'SEOUL CRO'
    Symyoo_CRO = 'Symyoo'
    Syneous_Health_CRO = 'Syneous Health'
    Synex_Consulting_CRO = 'Synex Consulting'
    UMT_CRO = 'UMT'
    MERCK_SHARP_DOHME_CRO = 'MSD'

    CHOICES = [
        (ADM_Korea_CRO, 'ADM Korea'),
        (AllLive_Healthcare_CRO, 'AllLive Healthcare'),
        (BDM_Consulting_CRO, 'BDM Consulting'),
        (BETHESDASOFT_CRO, 'BETHESDASOFT'),
        (C_R_Research_CRO, 'C&R Research'),
        (CALEB_MULTILAB_CRO, 'CALEB MULTILAB'),
        (CC_I_Research_CRO, 'CC&Research'),
        (CiKLux_CRO, 'CiKLux'),
        (Clinical_CRO_CRO, 'Clinical CRO'),
        (CliPS_CRO, 'CliPS'),
        (D2S_CRO, 'D2S'),
        (HELPTRIAL_CRO, 'HELPTRIAL'),
        (ICON_CRO, 'ICON'),
        (IQVIA_CRO,'IQVIA'),
        (JNPMEDI_CRO, 'JNPMEDI'),
        (KCSG_CRO, 'KCSG'),
        (KHMEDICARE_CRO, 'KHMEDICARE'),
        (Kolab_CRO, 'Kolab'),
        (LSK_Global_PS_CRO, 'LSK Global PS'),
        (Medi_Help_Line_CRO, 'Medi Help Line'),
        (Medical_Excellence_CRO, 'Medical Excellence'),
        (Medical_Writing_CRO, 'Medical Writing'),
        (PAREXEL_CRO, 'PAREXEL'),
        (PHARMACRO_CRO, 'PHARMACRO'),
        (PLS_CRO, 'PLS'),
        (PROMEDIS_CRO, 'PROMEDIS'),
        (Research_Mentor_CRO, 'Research Mentor'),
        (RNDMotiv_CRO, 'RNDMotiv'),
        (SEO_CHO_CRO_CRO, 'SEO-CHO CRO'),
        (SEOUL_CRO_CRO, 'SEOUL CRO'),
        (Symyoo_CRO, 'Symyoo'),
        (Syneous_Health_CRO, 'Syneous Health'),
        (Synex_Consulting_CRO, 'Synex Consulting'),
        (UMT_CRO, 'UMT'),
        (MERCK_SHARP_DOHME_CRO, 'MSD')
    ]

    class Meta:
        ordering = ['value']


class Vendor(ResearchFieldModel):
    IMEDIDATA = 'iMedidata'
    INFORM = 'InForm'
    ROCHE = 'Roche'
    VEEVAVAULT = 'veevavault'
    ORACLE_RDC = 'Oracle RDC'

    CHOICES = [
        (IMEDIDATA, 'iMedidata'),
        (INFORM, 'InForm'),
        (ROCHE, 'Roche'),
        (VEEVAVAULT, 'veevavault'),
        (ORACLE_RDC, 'Oracle RDC'),
    ]


class Research_Management(models.Model):
    research = models.ForeignKey(Research, on_delete=models.SET_NULL, null=True)
    cro = models.ForeignKey(CRO, on_delete=models.SET_NULL, null=True)
    vendor = models.ManyToManyField(Vendor)
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_field_value_and_text():
        m2m_field_list = [Vendor, CRO]
        ret = {}
        for c in m2m_field_list:
            c_lower_name = c.__name__.lower()
            choices = c.__dict__['CHOICES']
            ret[c_lower_name] = []
            for pk, choice in enumerate(choices):
                ret[c_lower_name].append(
                    (choice[0], choice[1])
                )
        return ret

    @staticmethod
    def create_field_value_and_text_dict():
        m2m_field_list = [Vendor]
        ret = {}
        for c in m2m_field_list:
            c_lower_name = c.__name__.lower()
            choices = c.__dict__['CHOICES']
            ret[c_lower_name] = {}
            for pk, choice in enumerate(choices):
                ret[c_lower_name][choice[0]] = choice[1]
        return ret

    def __str__(self):
        return f'{self.research}'

    @staticmethod
    def vendor_form_validation(request, research):
        errors = collections.defaultdict(list)

        # Get field values
        cro = CRO.objects.get(value=request.POST.get('cro'))
        vendor_types = request.POST.getlist('vendor')
        vendor = Vendor.objects.filter(value__in=vendor_types)

        temp_vendor = types.SimpleNamespace()
        temp_vendor.cro = cro
        temp_vendor.vendor = vendor
        temp_vendor.research = research
        return temp_vendor, errors


class Supporting_type(ResearchFieldModel):
    SAMPLE = 'sample'
    SEPARATE = 'separate blood draw'
    accompany = 'accompany blood draw'
    BLOOD = 'blood'
    CHOICES = (
        (SAMPLE, "진검 검체"),
        (SEPARATE, '별도 채혈'),
        (accompany, '채혈실 동행'),
        (BLOOD, '분주')
    )


class Supporting(models.Model):
    # attributes
    lab_date = models.DateTimeField(blank=True, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=False, null=True)
    kinds = models.CharField(max_length=50, choices=KINDS_CHOICES, blank=True, null=True)
    #pre_hour = models.CharField(max_length=2, blank=True, null=True)
    post_hour = models.CharField(max_length=2, blank=True, null=True)
    crc = models.CharField(max_length=50, blank=True, null=True)
    supporting_type = models.CharField(max_length=50, choices=SUPPORTING_TYPE_CHOICES, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    technician = models.CharField(max_length=50, blank=True, null=True)
    # meta
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    # relations


    @staticmethod
    def field_value_and_text():
        ret = {'kinds': KINDS_CHOICES, 'supporting_type': SUPPORTING_TYPE_CHOICES}
        return ret

    @staticmethod
    def create_field_value_and_text_dict():
        m2m_field_list = [Supporting_type]
        ret = {}
        for c in m2m_field_list:
            c_lower_name = c.__name__.lower()
            choices = c.__dict__['CHOICES']
            ret[c_lower_name] = {}
            for pk, choice in enumerate(choices):
                ret[c_lower_name][choice[0]] = choice[1]
        return ret

    @staticmethod
    def create_field_value_and_text():
        m2m_field_list = [Supporting_type]
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
    def supporting_form_validation(request):
        errors = collections.defaultdict(list)

        # Get field values
        lab_date_str = request.POST.get('lab_date', '')
        assignment_str = request.POST.get('assignment', '')
        if assignment_str != '':
            assignment = Assignment.objects.get(id=int(assignment_str))
        if assignment_str == '':
            assignment = None

        kinds = request.POST.get('kinds', '')
        #pre_hour = request.POST.get('pre_hour', '')
        post_hour = request.POST.get('post_hour', '')
        crc = request.POST.get('crc', '')
        #supporting_type_types = request.POST.getlist('supporting_type')
        #supporting_type = Supporting_type.objects.filter(value__in=supporting_type_types)
        supporting_type = request.POST.get('supporting_type', '')
        comment = request.POST.get('comment', '')
        technician = request.POST.get('technician', '')

        # convert to proper values
        kinds = KINDS_CHOICES_INV.get(kinds)
        supporting_type = SUPPORTING_TYPE_CHOICES_INV.get(supporting_type)

        try:
            lab_date = datetime.strptime(lab_date_str, '%Y/%m/%d %H:%M')
        except:
            lab_date = None

        if lab_date is None:
            errors['lab_date'].append('- 날짜를 선택하세요.')
        if assignment_str == '':
            errors['assignment'].append('- 환자를 선택하세요.')
        if kinds == 'PK-post' and not post_hour:
            errors['post_hour'].append('- PK-post 선택 시, post 시간 입력이 필수입니다.')

        temp_supporting = types.SimpleNamespace()
        temp_supporting.lab_date = lab_date
        temp_supporting.assignment = assignment
        temp_supporting.kinds = kinds
        #temp_supporting.pre_hour = pre_hour
        temp_supporting.post_hour = post_hour
        temp_supporting.crc = crc
        temp_supporting.supporting_type = supporting_type
        temp_supporting.comment = comment
        temp_supporting.technician = technician

        return temp_supporting, errors

    def __str__(self):
        return f'({self.id}) {self.assignment} | {self.lab_date} | CRC: {self.crc}, Technician: {self.technician}'


class Delivery(models.Model):
    # attributes
    visit_date = models.DateField(blank=True, null=True)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, blank=False, null=True)
    crc = models.CharField(max_length=50, blank=True, null=True)
    scheduled_time = models.CharField(max_length=50, choices=TIME_CHOICES, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    checking = models.CharField(max_length=1, blank=True, null=True)
    # meta
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    @staticmethod
    def field_value_and_text():
        ret = {'scheduled_time': TIME_CHOICES}
        return ret

    @staticmethod
    def delivery_form_validation(request):
        errors = collections.defaultdict(list)

        # Get field values
        visit_date_str = request.POST.get('visit_date', '')
        assignment_str = request.POST.get('assignment', '')
        if assignment_str != '':
            assignment = Assignment.objects.get(id=int(assignment_str))
        if assignment_str == '':
            assignment = None

        crc = request.POST.get('crc', '')
        scheduled_time = request.POST.get('scheduled_time', '')
        comment = request.POST.get('comment', '')
        checking = request.POST.get('checking', '')

        # convert to proper values
        scheduled_time = TIME_CHOICES_INV.get(scheduled_time)

        try:
            visit_date = datetime.strptime(visit_date_str, '%m/%d/%Y')
        except:
            visit_date = None

        if scheduled_time == '기타' and not comment:
            errors['comment'].append('- 기타 선택 시, comment 입력이 필수입니다.')

        temp_delivery = types.SimpleNamespace()
        temp_delivery.visit_date = visit_date
        temp_delivery.assignment = assignment
        temp_delivery.crc = crc
        temp_delivery.scheduled_time = scheduled_time
        temp_delivery.comment = comment
        temp_delivery.checking = checking

        return temp_delivery, errors

    def __str__(self):
        return f'{self.visit_date} {self.assignment}'


class QC_category(ResearchFieldModel):
    AE = 'AE'
    RECIST = 'RECIST'
    LAB = 'LAB'
    DOSAGE = 'DOSAGE'
    ERROR_ETC = 'ERROR_ETC'
    OMISSION_ETC = 'OMISSION_ETC'
    CYCLE = 'CYCLE'

    CHOICES = [
        (AE, '입력 오류 - AE 관련'),
        (RECIST, '입력 오류 - RECIST 관련'),
        (LAB, '입력 오류 - LAB 관련'),
        (DOSAGE, '입력 오류 - 투약 관련'),
        (ERROR_ETC, '입력 오류 - 기타'),
        (OMISSION_ETC, '입력 누락 - 기타'),
        (CYCLE, '입력 누락 - cycle'),
    ]


class QC(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, blank=False, null=True)
    research = models.ForeignKey(Research, on_delete=models.CASCADE, blank=False, null=True)
    crc = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    QC_category = models.ForeignKey(QC_category, on_delete=models.CASCADE, blank=False, null=True)
    QC_count = models.IntegerField(blank=False, null=True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    # meta
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_field_value_and_text_dict():
        m2m_field_list = [Vendor, QC_category]
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
    def QC_form_validation(request):
        errors = collections.defaultdict(list)

        # Get field values
        vendor_type = request.POST.get('vendor')
        vendor = Vendor.objects.filter(value=vendor_type).first()
        research_str = request.POST.get('research', '')
        research = Research.objects.get(id=int(research_str)) if research_str != '' else None
        crc_str = request.POST.get('crc', '')
        crc = Contact.objects.get(id=int(crc_str)) if crc_str != '' else None
        qc_category_type = request.POST.get('QC_category')
        qc_category = QC_category.objects.filter(value=qc_category_type).first()
        QC_count = request.POST.get('QC_count', '')
        start = request.POST.get('start', '')
        end = request.POST.get('end', '')

        #try:
        #    start = datetime.strptime(start_str, '%m/%d/%Y')
        #except:
        #    start = None

        #try:
        #    end = datetime.strptime(end_str, '%m/%d/%Y')
        #except:
        #    end = None

        temp_QC = types.SimpleNamespace()
        temp_QC.vendor = vendor
        temp_QC.research = research
        temp_QC.crc = crc
        temp_QC.QC_category = qc_category
        temp_QC.QC_count = QC_count
        temp_QC.start = start
        temp_QC.end = end

        return temp_QC, errors

    def __str__(self):
        return f'{self.vendor} -> {self.research}'
