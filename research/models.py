import json
import collections
import types
from datetime import datetime, date

from django.db import models
from django.contrib.auth.models import User
from user.models import Contact
from django.core.validators import MinValueValidator
from feedback.models import Feedback, STATUS_HISTORY, Assignment
from django.db.models import Q
from administration.models import Company


SEX_CHOICES = [
    ('M', 'M'),
    ('F', 'F'),
]
SEX_CHOICES_INV = {val: val for val, _ in SEX_CHOICES}

TEAM_CHOICES = [
    ('CLUE', 'CLUE'),
    ('GSI', 'GSI'),
    ('etc', 'etc'),
]
TEAM_CHOICES_INV = {val: val for val, _ in TEAM_CHOICES}

RECRUITING_CHOICES = [
    ('Recruiting', 'Recruiting'),
    ('Not yet recruiting', 'Not yet recruiting'),
    ('Completed', 'Completed'),
    ('Holding', 'Holding'),
]
RECRUITING_CHOICES_INV = {val: val for val, _ in RECRUITING_CHOICES}

YES_OR_NO_CHOICES = [
    ('Y', 'Y'),
    ('N', 'N'),
]
YES_OR_NO_CHOICES_INV = {val: val for val, _ in YES_OR_NO_CHOICES}

TYPE_CHOICES = [
    ('IIT', 'IIT'),
    ('SIT', 'SIT'),
    ('EAP', 'EAP'),
    ('PMS', 'PMS'),
    ('완화 연구', '완화 연구'),
    ('etc', 'etc'),
    ('IIT(기타/EAP)', 'IIT(기타/EAP)'),
]
TYPE_CHOICES_INV = {val: val for val, _ in TYPE_CHOICES}

STATUS_CHOICES = [
    ('종료보고완료', '종료 보고 완료'),
    ('결과보고완료', '결과 보고 완료'),
    ('장기보관완료', '장기 보관 완료'),
]
STATUS_CHOICES_INV = {val: val for val, _ in STATUS_CHOICES}

CANCER_CHOICES = [
    ('Stomach', 'Stomach cancer'),
    ('Sarcoma', 'Sarcoma'),
    ('CRC', 'Colorectal cancer'),
    ('Urological', 'Urological cancer'),
    ('Lung', 'Lung cancer'),
    ('Melanoma', 'Melanoma'),
    ('RCC', 'RCC'),
    ('Solid', 'Solid'),
    ('Solid(GC)', 'Solid(GC)'),
    ('Solid(Urological)', 'Solid(Urological)'),
    ('Phase1', 'Phase1')]

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


class Cancer(ResearchFieldModel):
    # 암종류 - 일단 폐암, 식도 암, 두경부암만으로 할거니깐 이거 3개만으로 해줘라
    NSCLC_CANCER = 'NSCLC'  # NSCLC
    SCLC_CANCER = 'SCLC'  # SCLC
    ESOPHAGEAL_CANCER = 'esophageal'  # 식도암
    HEAD_AND_NECK_CANCER = 'head_and_neck'  # 두경부암

    GASTRIC_CANCER = 'gastric'  # 위암
    SMALL_BOWEL_CANCER = 'small_bowel'  # 소장암
    COLORECTAL_CANCER = 'colorectal'  # 대장암

    HCC_CANCER = 'HCC'  # 간세포암
    GB_CANCER = 'GB'  # 담낭암
    BT_CANCER = 'BT'  # 담도암
    PANCREATIC_CANCER = 'pancreatic'  # 췌장암

    BREAST_CANCER = 'breast'  # 유방암
    OVARIAN_CANCER = 'ovarian'  # 난소암
    ENDOMETRIAL_CANCER = 'endometrial'  # 자궁내막
    VAGINAL_CANCER = 'vaginal'  # 질암
    CERVIX_CANCER = 'cervix'  # 자궁경부
    VULVA_CANCER = 'vulva'  # 외음부암

    KIDNEY_CANCER = 'kidney'  # 신장암
    URETER_CANCER = 'ureter'  # 요관암
    BLADDER_CANCER = 'bladder'  # 방광암
    PROSTATE_CANCER = 'prostate'  # 전립선암

    SARCOMA = 'sarcoma'  # 육종
    MELANOMA = 'melanoma'  # 흑색종
    ETC = 'etc'  # 기타
    PHASE1 = 'phase1'  # 1상
    Solid = 'Solid'  # 고형암

    NA = 'na'

    CHOICES = [
        (NA, '해당없음'),
        (NSCLC_CANCER, 'NSCLC'),
        (SCLC_CANCER, 'SCLC'),
        (ESOPHAGEAL_CANCER, 'Esophageal'),
        (HEAD_AND_NECK_CANCER, 'Head and Neck'),

        (GASTRIC_CANCER, 'Gastric'),
        (SMALL_BOWEL_CANCER, 'Small bowl'),
        (COLORECTAL_CANCER, 'Colorectal'),

        (HCC_CANCER, 'HCC'),
        (GB_CANCER, 'Gallbladder'),
        (BT_CANCER, 'Biliary tract'),
        (PANCREATIC_CANCER, 'Pancreatic'),

        (BREAST_CANCER, 'Breast'),
        (OVARIAN_CANCER, 'Ovary'),
        (ENDOMETRIAL_CANCER, 'Endometrial'),
        (VAGINAL_CANCER, 'Vaginal'),
        (CERVIX_CANCER, 'Cervix'),
        (VULVA_CANCER, 'Vulva'),

        (KIDNEY_CANCER, 'RCC'),
        (URETER_CANCER, 'Urothelial'),
        (BLADDER_CANCER, 'Bladder'),
        (PROSTATE_CANCER, 'CRPC'),

        (SARCOMA, 'Sarcoma'),
        (MELANOMA, 'Melanoma'),
        (PHASE1, '1상'),
        (ETC, '기타'),
        (Solid, 'Solid tumor')
    ]


class Lesion(ResearchFieldModel):
    # 측정가능한 병변 필요 여부  Measurable lesion, Evaluable lesion, No lesion에서 고르게
    REQUIRED = 'required'
    NOT_REQUIRED = 'not_required'
    NA = 'na'
    CHOICES = (
        (NA, "해당없음"),
        (REQUIRED, '필요'),
        (NOT_REQUIRED, '불필요')
    )


class Alternation(ResearchFieldModel):
    # 유전자 종류
    EGFR = "EGFR"
    HER2 = "HER2"
    ALK = "ALK"
    MET = "MET"
    NTRK = "NTRK"
    KRAS_NRAS = "KRAS/NRAS"
    BRAF_PR = "BRAF/PR"
    MSI = 'MSI'
    HRD = "HRD(BRCA/ATM/etc)"
    ER_PR = 'ER/PR'
    PIK3CA = "PIK3CA"
    FGFR = 'FGFR'
    TMB = 'TMB'
    NA = 'na'
    ETC = 'etc'
    CHOICES = (
        (NA, "해당없음"),
        (EGFR, "EGFR"),
        (HER2, "HER2"),
        (ALK, "ALK"),
        (MET, "MET"),
        (NTRK, "NTRK"),
        (KRAS_NRAS, "KRAS/NRAS"),
        (BRAF_PR, "BRAF/PR"),
        (MSI, 'MSI'),
        (HRD, "HRD(BRCA/ATM/etc)"),
        (ER_PR, "ER/PR"),
        (PIK3CA, "PIK3CA"),
        (FGFR, 'FGFR'),
        (TMB, 'TMB'),
        (ETC, '기타')
    )


class Line(ResearchFieldModel):
    # 몇번째 line 치료인지 - 보통 기준이 숫자로  1st line only, 2 ling only, 2~4line  있고
    # 치료 목제에 따라  neoadjuvant, adjuvant가 있음 다양하니 간호사들 입력에는 neoadjuvant,
    # adjuvant, 1,2,3, 4이상중에 고르게
    LINE1 = 'line1'
    LINE2 = 'line2'
    LINE3 = 'line3'
    LINE4_OR_MORE = 'line4_or_more'
    NEOADJUVANT = 'neoadjuvant'
    ADJUVANT = 'adjuvant'
    NA = 'na'
    PERIOP = 'periop'
    SOLID = 'solid'
    ETC = 'etc'
    CHOICES = (
        (NA, "해당없음"),
        (NEOADJUVANT, 'Neoadjuvant'),
        (ADJUVANT, 'Adjuvant'),
        (LINE1, 'Line 1'),
        (LINE2, 'Line 2'),
        (LINE3, 'Line 3'),
        (LINE4_OR_MORE, 'Line 4 or more'),
        (PERIOP, 'Periop'),
        (SOLID, 'Solid'),
        (ETC, '기타'),
    )


class Chemotherapy(ResearchFieldModel):
    # 기존에 항암 치료 - 간호사들은  platium based CTx, TKI, Immunotherapy, 중에고르게
    #CTX = 'CTx'
    #TKI = 'TKI'
    #IMMUNOTHERAPY = 'immunotherapy'
    #METABOLIC_ANTICANCER = 'metabolic anticancer'
    #OTHERS = 'others'
    #NA = 'na'
    #CHOICES = (
        #(NA, '해당없음'),
        #(CTX, 'CTx'),
        #(TKI, 'TKI'),
        #(IMMUNOTHERAPY, 'Immunotherapy'),
        #(METABOLIC_ANTICANCER, 'Antimetabolics'),
        #(OTHERS, 'Others')
    #)

    TOXIC = 'toxic_agent'
    TARGET = 'target_agent'
    IMMUNOTHERAPY = 'Immunotherapy'
    ETC = 'etc'
    CHOICES = (
        (TOXIC, 'toxic agent'),
        (TARGET, 'target agent'),
        (IMMUNOTHERAPY, 'Immunotherapy'),
        (ETC, '기타'),
    )


class IO_Naive(ResearchFieldModel):
    NAIVE = 'naive'
    EXPERIENCED = 'experienced'
    NA = 'na'
    CHOICES = (
        (NA, '해당없음'),
        (NAIVE, 'Naive'),
        (EXPERIENCED, 'Experienced')
    )


class PDL1(ResearchFieldModel):
    REQUIRED = 'required'
    NOT_REQUIRED = 'not_required'
    NA = 'na'
    CHOICES = (
        (NA, '해당없음'),
        (REQUIRED, '필요'),
        (NOT_REQUIRED, '불필요')
    )


class Brain_METS(ResearchFieldModel):
    POSSIBLE = 'possible'
    IMPOSSIBLE = 'impossible'
    NA = 'na'
    CHOICES = (
        (NA, '해당없음'),
        (POSSIBLE, '가능'),
        (IMPOSSIBLE, '불가능')
    )


class Biopsy(ResearchFieldModel):
    REQUIRED = 'required'
    NOT_REQUIRED = 'not_required'
    NA = 'na'
    CHOICES = (
        (NA, '해당없음'),
        (REQUIRED, '필요'),
        (NOT_REQUIRED, '불필요')
    )


class Phase(ResearchFieldModel):
    PHASE1 = 'phase1'
    PHASE2 = 'phase2'
    PHASE3 = 'phase3'
    PHASE4 = 'phase4'
    NA = 'na'
    CHOICES = (
        (NA, '해당없음'),
        (PHASE1, 'Phase 1'),
        (PHASE2, 'Phase 2'),
        (PHASE3, 'Phase 3'),
        (PHASE4, 'Phase 4'),
    )


class Type(ResearchFieldModel):
    IIT = 'IIT'
    SIT = 'SIT'
    EAP = 'EAP'
    PMS = 'PMS'
    Palliative = 'Palliative'
    Blood = 'Blood'
    ETC = 'ETC'
    CHOICES = (
        (IIT, 'IIT'),
        (SIT, 'SIT'),
        (EAP, 'EAP'),
        (PMS, 'PMS'),
        (Palliative, '완화연구'),
        (Blood, '혈액/조직연구'),
        (ETC, '기타')
    )


class Route_of_Administration(ResearchFieldModel):
    INTRAVENOUS = 'intravenous'
    INTRAMUSCULAR = 'intramuscular'
    SUBCUTANEOUS = 'subcutaneous'
    ORAL = 'oral'
    SUBLINGUAL = 'sublingual'
    INTRADERMAL = 'intradermal'
    CHOICES = (
        (INTRAVENOUS, 'Intravenous (IV)'),
        (INTRAMUSCULAR, 'Intramuscular (IM)'),
        (SUBCUTANEOUS, 'Subcutaneous (SC)'),
        (ORAL, 'Per Oral(PO)'),
        (SUBLINGUAL, 'Sublingual (SL)'),
        (INTRADERMAL, 'Intradermal (ID)'),
    )


class Research(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_deleted = models.BooleanField(default=False)

    onco_A = models.BooleanField(default=True)
    is_recruiting = models.CharField(choices=RECRUITING_CHOICES, null=True, max_length=50)
    is_pre_screening = models.CharField(choices=YES_OR_NO_CHOICES, null=True, max_length=50)
    #type = models.CharField(choices=TYPE_CHOICES, null=True, max_length=50)
    type = models.ManyToManyField(Type)
    route_of_administration = models.ManyToManyField(Route_of_Administration)
    status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=50)
    binder_location = models.CharField(max_length=500, null=True)
    study_coordinator = models.CharField(max_length=500, null=True)
    storage_date = models.DateField(blank=True, null=True)
    end_brief = models.DateField(blank=True, null=True) # 종료보고일
    result_brief = models.DateField(blank=True, null=True) # 결과보고일
    #CRA = models.CharField(max_length=200, null=True)
    CRO = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    CRA_name = models.CharField(max_length=200, null=True)
    CRA_phoneNumber = models.CharField(max_length=200, null=True)
    irb_number = models.CharField(max_length=200, null=True)
    cris_number = models.CharField(max_length=200, null=True)

    research_name = models.CharField(
        max_length=2000,
        null=True
    )
    study_code = models.CharField(
        max_length=100,
        null=True
    )
    research_explanation = models.CharField(
        max_length=2000,
        null=True,
        default=''
    )
    crc = models.ManyToManyField(Contact, related_name="crc")

    team = models.CharField(choices=TEAM_CHOICES, null=True, max_length=50)

    PI = models.CharField(
        max_length=2000,
        null=True
    )
    contact = models.CharField(
        max_length=2000,
        null=True
    )
    medicine_name = models.TextField(
        blank=True,
        null=True
    )
    arm_name = models.TextField(
        blank=True,
        null=True
    )
    first_backup = models.ForeignKey(Contact, on_delete=models.SET_NULL, related_name='first_backup', null=True)
    second_backup = models.ForeignKey(Contact, on_delete=models.SET_NULL, related_name='second_backup', null=True)

    # 암종류 - 일단 폐암, 식도 암, 두경부암만으로 할거니깐 이거 3개만으로 해줘라
    cancer = models.ManyToManyField(Cancer)
    # Phase
    phase = models.ManyToManyField(Phase)
    # 기존에 항암 치료 - 간호사들은  platium based CTx, TKI, Immunotherapy, 중에고르게
    chemotherapy = models.ManyToManyField(Chemotherapy)
    # 측정가능한 병변 필요 여부  Measurable lesion, Evaluable lesion, No lesion에서 고르게
    lesion = models.ForeignKey(Lesion, on_delete=models.SET_NULL, null=True)
    # 유전자 종류
    alternation = models.ManyToManyField(Alternation)
    # PDL1 수치 - Positive and Negative
    pdl1 = models.ForeignKey(PDL1, on_delete=models.SET_NULL, null=True)
    # IO Naive
    io_naive = models.ForeignKey(IO_Naive, on_delete=models.SET_NULL, null=True)
    # Brain METS 가능여부 Yes/No
    brain_mets = models.ForeignKey(Brain_METS, on_delete=models.SET_NULL,
                                   null=True)
    # Biopsy 가능여부 필요/불필요
    biopsy = models.ForeignKey(Biopsy, on_delete=models.SET_NULL, null=True)
    # 몇번째 line 치료인지 - 보통 기준이 숫자로  1st line only, 2 ling only, 2~4line  있고
    # 치료 목제에 따라  neoadjuvant, adjuvant가 있음 다양하니 간호사들 입력에는 neoadjuvant,
    # adjuvant, 1,2,3, 4이상중에 고르게
    line = models.ManyToManyField(Line)
    turn_around_time = models.IntegerField(validators=[
        MinValueValidator(0)
    ], null=True)
    # 간기능 - 간호사들만 입력, 기준치 입력
    liver_function = models.TextField(blank=True, null=True)
    # 폐기능- 간호사들 입력, 기준치 입력
    lung_function = models.TextField(blank=True, null=True)
    # 심장기능- 간호사들 입력, 기준치 입력
    heart_function = models.TextField(blank=True, null=True)
    # 신장기능-간호사들 입력 ,기준치 입력
    kidney_function = models.TextField(blank=True, null=True)
    # 비고
    remark = models.TextField(blank=True, null=True)
    # 생성 시간
    create_date = models.DateTimeField(auto_now_add=True)
    # 마지막 업데이트 시간
    update_date = models.DateTimeField(auto_now=True)

    @property
    def history(self):
        history = self.history_set.all().order_by('-create_date')
        for h in history:
            setattr(h, 'summary_json', h.summary)
        return history

    @staticmethod
    def create_field_value_and_text():
        m2m_field_list = [Cancer, Phase, Chemotherapy, Line, Alternation,
                          Lesion, PDL1, IO_Naive, Brain_METS, Biopsy, Type, Route_of_Administration]
        ret = {}
        for c in m2m_field_list:
            #c_name = c.__name__
            #c_upper_name = c.__name__.upper()
            c_lower_name = c.__name__.lower()
            choices = c.__dict__['CHOICES']
            ret[c_lower_name] = []
            for pk, choice in enumerate(choices):
                ret[c_lower_name].append(
                    [choice[0], choice[1]]
                )
        return ret

    @staticmethod
    def create_field_value_and_text_dict():
        m2m_field_list = [Cancer, Phase, Chemotherapy, Line, Alternation,
                          Lesion, PDL1, IO_Naive, Brain_METS, Biopsy, Type, Route_of_Administration]
        ret = {}
        for c in m2m_field_list:
            c_lower_name = c.__name__.lower()        # 'phase'
            choices = c.__dict__['CHOICES']          # (('na', '해당없음'), ('phase1', 'Phase 1'), ('phase2', 'Phase 2'), ('phase3', 'Phase 3'))
            ret[c_lower_name] = {}                   # {'phase': {}}
            for pk, choice in enumerate(choices):
                ret[c_lower_name][choice[0]] = choice[1]
        return ret    # {'phase': {'na': '해당없음', 'phase1': 'Phase 1', 'phase2': 'Phase 2', 'phase3': 'Phase 3'}}

    @staticmethod
    def create_field_id_and_text_dict():
        m2m_field = [Contact]
        ret = {}
        for c in m2m_field:
            c_lower_name = c.__name__.lower()
            #queryset = c.objects.filter(Q(onco_A=1) & ~Q(team__name='etc')).values('id', 'name')
            queryset = c.objects.filter(Q(onco_A=1)).filter(Q(user_id__groups__name='nurse') | Q(user_id__groups__name='medical records') | Q(user_id__groups__name='SETUP')).values('id', 'name')
            choices = tuple((str(q['id']), str(q['name'])) for q in queryset)
            ret[c_lower_name] = {}
            for pk, choice in enumerate(choices):
                ret[c_lower_name][choice[0]] = choice[1]
        return ret

    @staticmethod
    def contact_value_and_text():
        m2m_field_list = [Contact]
        ret = {}
        for c in m2m_field_list:
            c_lower_name = c.__name__.lower()
            #queryset = Contact.objects.filter(Q(onco_A=1) & ~Q(team__name='etc')).values('id', 'name').order_by('name')
            queryset = Contact.objects.filter(Q(onco_A=1))\
                .filter(Q(user_id__groups__name='nurse') |
                        Q(user_id__groups__name='medical records') |
                        Q(user_id__groups__name='SETUP') |
                        Q(user_id__groups__name='QC'))\
                .values('id', 'name').order_by('name')
            choices = tuple((str(q['id']), str(q['name'])) for q in queryset)
            ret[c_lower_name] = []
            for pk, choice in enumerate(choices):
                ret[c_lower_name].append([choice[0], choice[1]])
        return ret

    @staticmethod
    def contact_userID_and_text():
        ret = {}
        c_lower_name = Contact.__name__.lower()
        queryset = Contact.objects.filter(Q(onco_A=1))\
            .filter(Q(user_id__groups__name='nurse') |
                    Q(user_id__groups__name='medical records') |
                    Q(user_id__groups__name='SETUP') |
                    Q(user_id__groups__name='QC'))\
            .values('user_id', 'name').order_by('name')
        choices = tuple((str(q['user_id']), str(q['name'])) for q in queryset)
        ret[c_lower_name] = []
        for pk, choice in enumerate(choices):
            ret[c_lower_name].append([choice[0], choice[1]])
        return ret

    @staticmethod
    def get_field_name():
        return [
            #'ID',
            'Recruitment',
            #'Pre screening 진행 여부',
            #'유형',
            #'Status',
            #'바인더 위치',
            #'장기 보관 날짜',
            'Study Name',
            #'과제번호',
            #'임상시험 계획서 제목',
            #'IP',
            'CRC',
            #'CRC 연락처',
            #'백업 1',
            #'백업 2',
            #'TEAM',
            #'PI',
            'Cancer',
            'IIT/SIT',
            'Phase',
            #'Type of Therapy',
            #'Route of Administration',
            'Line',
            #'Alternation',
            #'Measurable Lesion 필요여부',
            #'PDL1 양성 필요여부',
            #'IO (면역치료) 사용력',
            #'Brain mets 환자 가능여부',
            #'Biopsy 필요여부',
            #'Turn around Time',
            #'Liver Function',
            #'Lung Function',
            #'Heart Function',
            #'Kidney Function',
            #'Remark'
        ]

    @staticmethod
    def research_form_validation(request):
        # POST req
        errors = collections.defaultdict(list)

        # Recruiting
        is_recruiting = request.POST.get('is_recruiting')
        is_recruiting = RECRUITING_CHOICES_INV.get(is_recruiting, None)

        # Pre screening
        is_pre_screening = request.POST.get('is_pre_screening')
        is_pre_screening = YES_OR_NO_CHOICES_INV.get(is_pre_screening, None)

        # Type
        type_types = request.POST.getlist('type')
        type = Type.objects.filter(value__in=type_types)

        # Route of Administration
        route_of_administrations = request.POST.getlist('route_of_administration')
        route_of_administration = Route_of_Administration.objects.filter(value__in=route_of_administrations)

        # Status
        status = request.POST.get('status')
        status = STATUS_CHOICES_INV.get(status, None)

        # 바인더 위치
        binder_location = request.POST.get('binder_location', None)

        # 바인더 위치
        study_coordinator = request.POST.get('study_coordinator', None)

        # 장기 보관 날짜
        storage_date_str = request.POST.get('storage_date', '')

        # 종료 보관 날짜
        end_brief_str = request.POST.get('end_brief', '')

        # 결과 보관 날짜
        result_brief_str = request.POST.get('result_brief', '')

        # CRA 관련
        #CRA = request.POST.get('CRA', None)
        CRO_str = request.POST.get('CRO', '')
        if CRO_str != '':
            CRO = Company.objects.get(id=int(CRO_str))
        if CRO_str == '':
            CRO = None

        CRA_name = request.POST.get('CRA_name', None)
        CRA_phoneNumber = request.POST.get('CRA_phoneNumber', None)

        # IRB No.
        irb_number = request.POST.get('irb_number', None)

        # CRIS No.
        cris_number = request.POST.get('cris_number', None)

        # Research Name
        research_name = request.POST.get('research_name', None)

        # Study Code
        study_code = request.POST.get('study_code', None)

        # Research Explanation
        research_explanation = request.POST.get('research_explanation', None)

        # CRC
        crc_types = request.POST.getlist('crc')
        #crc = Contact.objects.filter(id__in=crc_types)
        crc = Contact.objects.filter(id__in=crc_types)

        # TEAM
        team = request.POST.get('team')
        #team = TEAM_CHOICES_INV.get(team, None)

        # PI
        PI = request.POST.get('PI', None)

        # Contact
        contact = request.POST.get('contact', None)

        # Medicine Name
        medicine_name = request.POST.get('medicine_name', None)

        # ARM Name
        arm_name = request.POST.get('arm_name', None)

        # first & second backup
        first_backup_str = request.POST.get('first_backup', '')
        if first_backup_str != '':
            first_backup = Contact.objects.get(id=int(first_backup_str))
        if first_backup_str == '':
            first_backup = None

        second_backup_str = request.POST.get('second_backup', '')
        if second_backup_str != '':
            second_backup = Contact.objects.get(id=int(second_backup_str))
        if second_backup_str == '':
            second_backup = None

        # Cancer
        cancer_types = request.POST.getlist('cancer')
        cancer = Cancer.objects.filter(value__in=cancer_types)

        # Phase
        phase_types = request.POST.getlist('phase')
        phase = Phase.objects.filter(value__in=phase_types)

        # Leison
        #lesion_type = request.POST.get('lesion')
        #lesion = Lesion.objects.filter(value=lesion_type).first()

        # Alternation
        #alternation_types = request.POST.getlist('alternation')
        #alternation = Alternation.objects.filter(value__in=alternation_types)

        # PDL1
        #pdl1_type = request.POST.get('pdl1')
        #pdl1 = PDL1.objects.filter(value=pdl1_type).first()

        # Line
        line_types = request.POST.getlist('line')
        line = Line.objects.filter(value__in=line_types)

        # Chemotherapy
        #chemotherapy_types = request.POST.getlist('chemotherapy')
        #chemotherapy = Chemotherapy.objects.filter(value__in=chemotherapy_types)

        # IO Naive
        #io_naive_type = request.POST.get('io_naive')
        #io_naive = IO_Naive.objects.filter(value=io_naive_type).first()

        # Brain METS
        #brain_mets_type = request.POST.get('brain_mets')
        #brain_mets = Brain_METS.objects.filter(value=brain_mets_type).first()

        # Biopsy
        #biopsy_type = request.POST.get('biopsy')
        #biopsy = Biopsy.objects.filter(value=biopsy_type).first()

        # Period
        #turn_around_time_str = request.POST['turn_around_time']
        #turn_around_time = None if (
        #        turn_around_time_str is None or turn_around_time_str == '') \
        #    else int(turn_around_time_str)

        # Functions and remark
        #liver_func = request.POST['liver-function']
        #lung_func = request.POST['lung-function']
        #heart_func = request.POST['heart-function']
        #kidney_func = request.POST['kidney-function']
        remark = request.POST['remark']

        try:
            storage_date = datetime.strptime(storage_date_str, '%m/%d/%Y')
        except:
            storage_date = None
        try:
            end_brief = datetime.strptime(end_brief_str, '%m/%d/%Y')
        except:
            end_brief = None
        try:
            result_brief = datetime.strptime(result_brief_str, '%m/%d/%Y')
        except:
            result_brief = None

        # Validation
        if not research_name:
            errors['research_name'].append('- 연구 이름을 입력하세요.')
        #if not study_code:
        #    errors['study_code'].append('- 연구 과제번호를 입력하세요.')
        if not is_recruiting:
            errors['is_recruiting'].append('- Recruiting 여부를 선택하세요.')
        if not is_pre_screening:
            errors['is_pre_screening'].append('- Pre screening 여부를 선택하세요.')
        if not type_types:
            errors['type'].append('- 연구 유형을 선택하세요.')
        if 'IIT' in type_types and 'SIT' in type_types:
            errors['type'].append('- 유형 (필수) 항목은 하나의 값만 선택되어야 합니다.')
        if 'SIT' in type_types and not CRO:
            errors['CRO'].append('- SIT 연구의 경우, 필수 입력입니다.')
        #if not research_explanation:
        #    errors['research_explanation'].append('- 연구 부연 설명을 입력하세요.')
        #if not crc_types:
        #    errors['crc'].append('- 담당 간호사 이름을 입력하세요.')
        if not team:
            errors['team'].append('- 담당 간호사의 소속을 선택하세요.')
        if not PI:
            errors['PI'].append('- PI 이름을 입력하세요.')
        if not contact:
            errors['contact'].append('- 담당 간호사 연락처를 입력하세요.')
        if not medicine_name:
            errors['medicine_name'].append('- 약 이름을 입력하세요.')
        #if first_backup_str == '':
        #    errors['first_backup'].append('- 하나의 값은 선택되어야합니다.')
        #if second_backup_str == '':
        #    errors['second_backup'].append('- 하나의 값은 선택되어야합니다.')
        #if first_backup_str == second_backup_str:
        #    errors['second_backup'].append('- 백업 1과 다른 값이 선택되어야합니다.')
        #if not cancer_types:
        #    errors['cancer'].append('- 하나의 값은 선택되어야합니다.')
        #if not phase_types:
        #    errors['phase'].append('- 하나의 값은 선택되어야합니다.')
        #if not chemotherapy_types:
        #    errors['chemotherapy'].append('- 하나의 값은 선택되어야합니다.')
        #if not lesion_type:
        #    errors['lesion'].append('- 하나의 값은 선택되어야합니다.')
        #if not alternation_types:
        #    errors['alternation'].append('- 하나의 값은 선택되어야합니다.')
        #if not pdl1:
        #    errors['pdl1'].append('- 최소 하나의 값은 선택되어야합니다.')
        #if not line_types:
        #    errors['line'].append('- 하나의 값은 선택되어야합니다.')
        #if not io_naive:
        #    errors['io_naive'].append('- 하나의 값은 선택되어야합니다.')
        #if not brain_mets:
        #    errors['brain_mets'].append('- 최소 하나의 값은 선택되어야합니다.')
        #if not biopsy:
        #    errors['biopsy'].append('- 최소 하나의 값은 선택되어야합니다.')
        #if not turn_around_time:
        #    errors['turn_around_time'].append('- 기간을 입력하세요.')

        temp_research = types.SimpleNamespace()
        temp_research.is_recruiting = is_recruiting
        temp_research.is_pre_screening = is_pre_screening
        temp_research.type = type
        temp_research.route_of_administration = route_of_administration
        temp_research.status = status
        temp_research.binder_location = binder_location
        temp_research.study_coordinator = study_coordinator
        temp_research.storage_date = storage_date
        temp_research.end_brief = end_brief
        temp_research.result_brief = result_brief
        #temp_research.CRA = CRA
        temp_research.CRO = CRO
        temp_research.CRA_name = CRA_name
        temp_research.CRA_phoneNumber = CRA_phoneNumber
        temp_research.irb_number = irb_number
        temp_research.cris_number = cris_number
        temp_research.research_name = research_name
        temp_research.study_code = study_code
        temp_research.research_explanation = research_explanation
        temp_research.crc = crc
        temp_research.team = team
        temp_research.PI = PI
        temp_research.contact = contact
        temp_research.medicine_name = medicine_name
        temp_research.arm_name = arm_name
        temp_research.first_backup = first_backup
        temp_research.second_backup = second_backup
        temp_research.cancer = cancer
        temp_research.phase = phase
        #temp_research.lesion = lesion
        #temp_research.alternation = alternation
        #temp_research.pdl1 = pdl1
        temp_research.line = line
        #temp_research.chemotherapy = chemotherapy
        #temp_research.io_naive = io_naive
        #temp_research.brain_mets = brain_mets
        #temp_research.biopsy = biopsy
        #temp_research.turn_around_time = turn_around_time

        #liver_function = None if liver_func.strip() == '' else liver_func
        #lung_function = None if lung_func.strip() == '' else lung_func
        #heart_function = None if heart_func.strip() == '' else heart_func
        #kidney_function = None if kidney_func.strip() == '' else kidney_func
        remark = None if remark.strip() == '' else remark

        #temp_research.liver_function = liver_function
        #temp_research.lung_function = lung_function
        #temp_research.heart_function = heart_function
        #temp_research.kidney_function = kidney_function
        temp_research.remark = remark

        return temp_research, errors

    def tolist(self):
        m2m_field_list = [Cancer, Phase, Alternation, Line, Chemotherapy, Contact, Type, Route_of_Administration]

        ret = {}
        for c in m2m_field_list:
            if c != Contact:
                c_lower_name = c.__name__.lower()
                ret[c_lower_name] = [t.inv_choices[getattr(t, 'value')] for t in getattr(self, c_lower_name).all()]
            else:
                ret['crc'] = [t.inv_choices[getattr(t, 'name')] for t in getattr(self, 'crc').all()]

        return list(map(str, [
            # self.id,
            self.is_recruiting,
            #self.is_pre_screening,
            #', '.join(ret['type']),
            # ', '.join(ret['route_of_administration']),
            #self.status,
            #self.binder_location,
            #self.study_coordinator,
            #self.storage_date,
            #self.end_brief,
            #self.result_brief,
            #self.CRA,
            #self.CRO,
            #self.CRA_name,
            #self.CRA_phoneNumber,
            #self.irb_number,
            #self.cris_number,
            self.research_name,
            #self.study_code,
            #self.research_explanation,
            #self.medicine_name,
            #self.arm_name,
            ', '.join(ret['crc']),
            #self.contact,
            #self.first_backup,
            #self.second_backup,
            #self.team,
            #self.PI,
            ', '.join(ret['cancer']),
            ', '.join(ret['type']),
            ', '.join(ret['phase']),
            #', '.join(ret['chemotherapy']),
            ', '.join(ret['line']),
            #', '.join(ret['alternation']),
            #self.lesion,
            #self.pdl1,
            #self.io_naive,
            #self.brain_mets,
            #self.biopsy,
            #self.turn_around_time,
            #self.liver_function if self.liver_function else '(비어있음)',
            #self.lung_function if self.lung_function else '(비어있음)',
            #self.heart_function if self.heart_function else '(비어있음)',
            #self.kidney_function if self.kidney_function else '(비어있음)',
            #self.remark if self.remark else '(비어있음)'
        ]))

    def json(self):
        research = {}
        research['id'] = self.id
        research['is_deleted'] = self.is_deleted
        research['onco_A'] = self.onco_A
        research['is_recruiting'] = self.is_recruiting
        research['is_pre_screening'] = self.is_pre_screening
        research['type'] = self.type
        research['route_of_administration'] = self.route_of_administration
        research['status'] = self.status
        research['binder_location'] = self.binder_location
        research['study_coordinator'] = self.study_coordinator
        research['storage_date'] = self.storage_date
        research['end_brief'] = self.end_brief
        research['result_brief'] = self.result_brief
        #research['CRA'] = self.CRA
        research['CRO'] = self.CRO
        research['CRA_name'] = self.CRA_name
        research['CRA_phoneNumber'] = self.CRA_phoneNumber
        research['irb_number'] = self.irb_number
        research['cris_number'] = self.cris_number
        research['research_name'] = self.research_name
        research['study_code'] = self.study_code
        research['research_explanation'] = self.research_explanation
        research['team'] = self.team
        research['PI'] = self.PI
        research['contact'] = self.contact
        research['medicine_name'] = self.medicine_name
        research['arm_name'] = self.arm_name
        research['first_backup'] = self.first_backup
        research['second_backup'] = self.second_backup
        research['pdl1'] = self.pdl1
        research['lesion'] = self.lesion
        research['io_naive'] = self.io_naive
        research['brain_mets'] = self.brain_mets
        research['biopsy'] = self.biopsy
        research['turn_around_time'] = self.turn_around_time
        research['liver_function'] = self.liver_function
        research['lung_function'] = self.lung_function
        research['heart_function'] = self.heart_function
        research['kidney_function'] = self.kidney_function
        research['remark'] = self.remark

        m2m_field_list = [Cancer, Phase, Alternation, Line, Chemotherapy, Contact, Type, Route_of_Administration]
        for c in m2m_field_list:
            if c != Contact:
                c_lower_name = c.__name__.lower()
                research[c_lower_name] = []
                research[c_lower_name + '_values'] = []
                for t in getattr(self, c_lower_name).all():
                    _json = t.json()
                    research[c_lower_name].append(_json)
                    research[c_lower_name + '_values'].append(_json['type'])
            else:
                research['crc'] = []
                research['crc_values'] = []
                for t in getattr(self, 'crc').all():
                    _json = t.json()
                    research['crc'].append(_json)
                    research['crc_values'].append(_json['type'])

        research['file'] = [f.json() for f in self.uploadfile_set.all()]
        research['eng_file'] = [f.json() for f in self.uploadengfile_set.all()]
        research['inclusion'] = [f.json() for f in self.uploadinclusion_set.all()]
        research['exclusion'] = [f.json() for f in self.uploadexclusion_set.all()]
        research['reference'] = [f.json() for f in self.uploadreference_set.all()]
        research['image'] = [i.json() for i in self.uploadimage_set.all()]
        research['archive'] = [i.json() for i in self.research_archive_set.all()]
        research['history'] = [h.json() for h in
                               self.history_set.all().order_by('-create_date')]
        return research

    def __str__(self):
        return '(' + str(self.id) + ') ' + self.research_name


    def edited_assign_status(self):
        return STATUS_HISTORY.objects.filter(assignment__research_id=self.id, assignment__is_deleted=0)

    def assign_status(self):
        return Feedback.objects.filter(assignment__research_id=self.id, assignment__is_deleted=0)

    def assignment(self):
        return Assignment.objects.filter(research_id=self.id, is_deleted=0)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'research/{0}/protocol_ko/{1}'.format(instance.research.id, filename)

class UploadFile(models.Model): # 프로토콜(국문)
    is_deleted = models.BooleanField(default=False)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    filename = models.CharField(max_length=800)
    file = models.FileField(upload_to=user_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.file.url,
            'research': self.research.id,
            'filename': self.filename
        }

def uploadengfile_directory_path(instance, filename):
    return 'research/{0}/protocol_eng/{1}'.format(instance.research.id, filename)

class UploadEngFile(models.Model): # 프로토콜 (영문)
    is_deleted = models.BooleanField(default=False)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    filename = models.CharField(max_length=800)
    file = models.FileField(upload_to=uploadengfile_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.file.url,
            'research': self.research.id,
            'filename': self.filename
        }

def uploadinclusion_directory_path(instance, filename):
    return 'research/{0}/inclusion/{1}'.format(instance.research.id, filename)

class UploadInclusion(models.Model): # 주 선정기준 이미지
    is_deleted = models.BooleanField(default=False)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    filename = models.CharField(max_length=800)
    file = models.FileField(upload_to=uploadinclusion_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.file.url,
            'research': self.research.id,
            'filename': self.filename
        }

def uploadexclusion_directory_path(instance, filename):
    return 'research/{0}/exclusion/{1}'.format(instance.research.id, filename)

class UploadExclusion(models.Model): # 주 제외기준 이미지
    is_deleted = models.BooleanField(default=False)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    filename = models.CharField(max_length=800)
    file = models.FileField(upload_to=uploadexclusion_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.file.url,
            'research': self.research.id,
            'filename': self.filename
        }

def uploadreference_directory_path(instance, filename):
    return 'research/{0}/reference/{1}'.format(instance.research.id, filename)

class UploadReference(models.Model):  # Reference
    is_deleted = models.BooleanField(default=False)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    filename = models.CharField(max_length=800)
    file = models.FileField(upload_to=uploadreference_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.file.url,
            'research': self.research.id,
            'filename': self.filename
        }

def research_binder_image_directory_path(instance, filename):
    return 'binder_image/research/{0}/{1}'.format(instance.research.id, filename)

class UploadImage(models.Model): # 바인더 이미지 (위치)
    is_deleted = models.BooleanField(default=False)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    imagename = models.CharField(max_length=800)
    image = models.ImageField(upload_to=research_binder_image_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.image.url,
            'research': self.research.id,
            'imagename': self.imagename
        }

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.research} -> {self.imagename}'


class History(models.Model):
    CREATE_RESEARCH = 'create_research'
    EDIT_RESEARCH = 'edit_research'
    REMOVE_RESEARCH = 'remove_research'
    ASSIGN_PATIENT = 'assign_patient'
    REMOVE_PATIENT = 'remove_patient'
    CHOICES = (
        (CREATE_RESEARCH, '연구 생성'),
        (EDIT_RESEARCH, '연구 수정'),
        (REMOVE_RESEARCH, '연구 삭제'),
        (ASSIGN_PATIENT, '환자 배정'),
        (REMOVE_PATIENT, '환자 삭제'),
    )
    INV_CHOICES = {value: text for value, text in CHOICES}

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                             blank=True)
    research = models.ForeignKey(Research, on_delete=models.SET_NULL, null=True,
                                 blank=True)
    patient = models.ForeignKey(Feedback, on_delete=models.SET_NULL,
                                null=True, blank=True)
    history_type = models.CharField(
        max_length=150,
        choices=CHOICES,
        null=False
    )
    summary = models.JSONField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)

    def json(self):
        return {
            'id': self.id,
            'user': {
                'username': self.user.username,
            },
            'research': {
                'id': self.research.id,
                'research_name': self.research.research_name,
                'medicine_name': self.research.medicine_name,
            },
            # 'patient': None if self.patient is None else self.patient.id,
            'history_type': self.history_type,
            'summary': self.summary,
            'create_date': self.create_date
        }


class WaitingList(models.Model):
    register_number = models.IntegerField(blank=False)
    name = models.CharField(max_length=10, blank=False)
    doctor = models.CharField(max_length=10, null=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, null=True)
    age = models.IntegerField(blank=False, null=True)
    curr_status = models.TextField(max_length=500, null=True)
    # mata
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    # relations
    phase = models.ForeignKey(Phase, on_delete=models.SET_NULL, blank=True, null=True)
    cancer = models.ForeignKey(Cancer, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)

    @property
    def history(self):
        history = self.history_set.all().order_by('-create_date')
        for h in history:
            setattr(h, 'summary_json', h.summary)
        return history

    @staticmethod
    def field_value_and_text():
        ret = {'sex': SEX_CHOICES}
        return ret

    @staticmethod
    def waitinglist_form_validation(request, cancer):
        errors = collections.defaultdict(list)

        # Get field values
        register_number = request.POST.get('register_number')
        name = request.POST.get('name')
        doctor = request.POST.get('doctor')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        curr_status = request.POST.get('curr_status')

        # convert to proper values
        sex = SEX_CHOICES_INV.get(sex, None)
        register_number = None if not register_number else int(register_number)
        age = None if not age else int(age)

        if not register_number:
            errors['register_number'].append('- 환자 등록번호를 입력하세요.')
        if not name:
            errors['name'].append('- 이름을 입력하세요.')
        #if not doctor:
        #    errors['doctor'].append('- 주치의를 입력하세요.')
        #if sex is None:
        #    errors['sex'].append('- 성별을 선택하세요.')
        #if not age:
        #    errors['age'].append('- 나이를 입력하세요.')

        temp_waitinglist = types.SimpleNamespace()
        temp_waitinglist.register_number = register_number
        temp_waitinglist.name = name
        temp_waitinglist.doctor = doctor
        temp_waitinglist.sex = sex
        temp_waitinglist.age = age
        temp_waitinglist.curr_status = curr_status
        temp_waitinglist.cancer = cancer
        temp_waitinglist.user = request.user

        return temp_waitinglist, errors

    @staticmethod
    def waitinglist_PI_form_validation(request):
        errors = collections.defaultdict(list)

        # Get field values
        if 'cancer' in request.POST:
            cancer_types = request.POST.getlist('cancer')
            cancer = Cancer.objects.filter(value__in=cancer_types)[0]
        else:
            cancer = request.POST.get('cancer', None)

        if 'phase' in request.POST:
            phase_types = request.POST.getlist('phase')
            phase = Phase.objects.filter(value__in=phase_types)[0]
        else:
            phase = request.POST.get('phase', None)

        register_number = request.POST.get('register_number')
        name = request.POST.get('name')
        doctor = request.POST.get('doctor')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        curr_status = request.POST.get('curr_status')

        # convert to proper values
        sex = SEX_CHOICES_INV.get(sex, None)
        register_number = None if not register_number else int(register_number)
        age = None if not age else int(age)

        if cancer is None and phase is None:
            errors['cancer'].append('- Cancer을 선택하세요.')
        if not register_number:
            errors['register_number'].append('- 환자 등록번호를 입력하세요.')
        if not name:
            errors['name'].append('- 이름을 입력하세요.')
        #if not doctor:
        #    errors['doctor'].append('- 주치의를 입력하세요.')
        #if sex is None:
        #    errors['sex'].append('- 성별을 선택하세요.')
        #if not age:
        #    errors['age'].append('- 나이를 입력하세요.')

        temp_waitinglist = types.SimpleNamespace()
        temp_waitinglist.cancer = cancer
        temp_waitinglist.phase = phase
        temp_waitinglist.register_number = register_number
        temp_waitinglist.name = name
        temp_waitinglist.doctor = doctor
        temp_waitinglist.sex = sex
        temp_waitinglist.age = age
        temp_waitinglist.curr_status = curr_status
        temp_waitinglist.cancer = cancer
        temp_waitinglist.user = request.user

        return temp_waitinglist, errors

    @staticmethod
    def phase_waitinglist_form_validation(request, phase):
        errors = collections.defaultdict(list)

        # Get field values
        register_number = request.POST.get('register_number')
        name = request.POST.get('name')
        doctor = request.POST.get('doctor')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        curr_status = request.POST.get('curr_status')

        # convert to proper values
        sex = SEX_CHOICES_INV.get(sex, None)
        register_number = None if not register_number else int(register_number)
        age = None if not age else int(age)

        if not register_number:
            errors['register_number'].append('- 환자 등록번호를 입력하세요.')
        if not name:
            errors['name'].append('- 이름을 입력하세요.')

        temp_waitinglist = types.SimpleNamespace()
        temp_waitinglist.register_number = register_number
        temp_waitinglist.name = name
        temp_waitinglist.doctor = doctor
        temp_waitinglist.sex = sex
        temp_waitinglist.age = age
        temp_waitinglist.curr_status = curr_status
        temp_waitinglist.phase = phase
        temp_waitinglist.user = request.user

        return temp_waitinglist, errors

    def __str__(self):
        return f'({self.id}) {self.register_number} {self.name} -> {self.cancer}'


class research_WaitingList(models.Model):
    register_number = models.IntegerField(blank=False)
    name = models.CharField(max_length=10, blank=False)
    doctor = models.CharField(max_length=10, null=True)
    sex = models.CharField(choices=SEX_CHOICES, max_length=1, null=True)
    age = models.IntegerField(blank=False, null=True)
    curr_status = models.TextField(max_length=500, null=True)
    # mata
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    # relations
    research = models.ForeignKey(Research, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=False, null=True)

    @property
    def history(self):
        history = self.history_set.all().order_by('-create_date')
        for h in history:
            setattr(h, 'summary_json', h.summary)
        return history

    @staticmethod
    def field_value_and_text():
        ret = {'sex': SEX_CHOICES}
        return ret

    @staticmethod
    def research_waitinglist_form_validation(request, research):
        errors = collections.defaultdict(list)

        # Get field values
        register_number = request.POST.get('register_number')
        name = request.POST.get('name')
        doctor = request.POST.get('doctor')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        curr_status = request.POST.get('curr_status')

        # convert to proper values
        sex = SEX_CHOICES_INV.get(sex, None)
        register_number = None if not register_number else int(register_number)
        age = None if not age else int(age)

        if not register_number:
            errors['register_number'].append('- 환자 등록번호를 입력하세요.')
        if not name:
            errors['name'].append('- 이름을 입력하세요.')

        temp_waitinglist = types.SimpleNamespace()
        temp_waitinglist.register_number = register_number
        temp_waitinglist.name = name
        temp_waitinglist.doctor = doctor
        temp_waitinglist.sex = sex
        temp_waitinglist.age = age
        temp_waitinglist.curr_status = curr_status
        temp_waitinglist.research = research
        temp_waitinglist.user = request.user

        return temp_waitinglist, errors

    def __str__(self):
        return f'({self.id}) {self.register_number} {self.name} -> {self.research.research_name}'



class ONCO_CR_COUNT(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE, blank=True, null=False)
    r_target = models.CharField(max_length=50, blank=True, null=False)
    cancer = models.ManyToManyField(Cancer)

    @staticmethod
    def create_field_value_and_text_dict():
        m2m_field_list = [Cancer]
        ret = {}
        for c in m2m_field_list:
            c_lower_name = c.__name__.lower()
            choices = c.__dict__['CHOICES']
            ret[c_lower_name] = {}
            for pk, choice in enumerate(choices):
                ret[c_lower_name][choice[0]] = choice[1]
        return ret

    def __str__(self):
        return f'{self.research.research_name} -> Cancer: {self.cancer} / Target: {self.r_target}'


class Pre_Initiation(models.Model):
    team = models.CharField(choices=TEAM_CHOICES, null=True, max_length=50)
    study_code = models.CharField(max_length=100, null=True)
    pre_research_name = models.CharField(max_length=100, blank=True, null=False)
    study_explanation = models.CharField(max_length=2000, null=True)
    #type = models.CharField(choices=TYPE_CHOICES, nullTrue, max_length=50)
    type = models.ManyToManyField(Type)
    set_up = models.ManyToManyField(Contact)
    PI = models.CharField(max_length=100, blank=True, null=False)
    crc = models.CharField(max_length=100, blank=True, null=False)
    is_withhold = models.CharField(choices=YES_OR_NO_CHOICES, null=True, max_length=50, default='N')
    is_commence = models.CharField(choices=YES_OR_NO_CHOICES, null=True, max_length=50, default='N')
    tx = models.CharField(max_length=500, blank=True, null=True)

    cancer = models.ManyToManyField(Cancer)
    phase = models.ManyToManyField(Phase)
    chemotherapy = models.ManyToManyField(Chemotherapy)
    alternation = models.ManyToManyField(Alternation)
    sponsor = models.CharField(max_length=100, null=True)  # SIT: 의뢰사, IIT: Company or CI
    CRO = models.CharField(max_length=100, null=True)      # SIT만 해당
    initiation_date = models.DateField(blank=True, null=True)
    CTC_contract = models.BooleanField(default=False, blank=True, null=True)
    CTC_non_contract_reason = models.TextField(blank=True, null=False)
    memo = models.TextField(blank=True, null=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    @property
    def history(self):
        history = self.pre_initiation_set.all().order_by('-create_date')
        for h in history:
            setattr(h, 'summary_json', h.summary)
        return history

    @staticmethod
    def pre_initiation_form_validation(request):
        errors = collections.defaultdict(list)

        # Get field values
        team = request.POST.get('team')
        study_code = request.POST.get('study_code')
        pre_research_name = request.POST.get('pre_research_name')
        study_explanation = request.POST.get('study_explanation')
        #type = request.POST.get('type')
        #type = TYPE_CHOICES_INV.get(type, None)
        type_types = request.POST.getlist('type')
        type = Type.objects.filter(value__in=type_types)
        set_up_types = request.POST.getlist('set_up')
        set_up = Contact.objects.filter(name__in=set_up_types)
        PI = request.POST.get('PI')
        crc = request.POST.get('crc')
        is_withhold = request.POST.get('is_withhold')
        is_withhold = YES_OR_NO_CHOICES_INV.get(is_withhold, None)
        is_commence = request.POST.get('is_commence')
        is_commence = YES_OR_NO_CHOICES_INV.get(is_commence, None)
        tx = request.POST.get('tx')

        cancer_types = request.POST.getlist('cancer')
        cancer = Cancer.objects.filter(value__in=cancer_types)
        phase_types = request.POST.getlist('phase')
        phase = Phase.objects.filter(value__in=phase_types)
        #chemotherapy_types = request.POST.getlist('chemotherapy')
        #chemotherapy = Chemotherapy.objects.filter(value__in=chemotherapy_types)
        #alternation_types = request.POST.getlist('alternation')
        #alternation = Alternation.objects.filter(value__in=alternation_types)
        sponsor = request.POST.get('sponsor')
        CRO = request.POST.get('CRO')
        initiation_date_str = request.POST.get('initiation_date', '')
        CTC_contract = True if request.POST.get('CTC_contract') == 'on' else False
        CTC_non_contract_reason = request.POST.get('CTC_non_contract_reason')
        memo = request.POST.get('memo')

        try:
            initiation_date = datetime.strptime(initiation_date_str, '%m/%d/%Y')
        except:
            initiation_date = None

        if not pre_research_name:
            errors['pre_research_name'].append('- 연구명을 입력하세요.')
        if not type_types:
            errors['type'].append('- 연구 유형을 선택하세요.')
        if 'IIT' in type_types and 'SIT' in type_types:
            errors['type'].append('- 유형 (필수) 항목은 하나의 값만 선택되어야 합니다.')
        if team is None:
            errors['team'].append('- team을 선택하세요.')
        if not cancer_types:
            errors['cancer'].append('- 하나의 값은 선택되어야합니다.')
        if not sponsor:
            errors['sponsor'].append('- SIT의 경우 의뢰사, IIT의 경우 Comapny 또는 CI를 입력해 주세요.')
        # 2022/10/20부터 적용
        if 'SIT' in type_types and CTC_contract is False and not CTC_non_contract_reason and initiation_date is not None \
                and date(initiation_date.year, initiation_date.month, initiation_date.day) > date(2022,10,20):
            errors['CTC_contract'].append('- CTC 주사실 계약 여부를 선택하세요. 예외 사항의 경우, 사유를 입력하여 주시기 바랍니다.')

        temp_pre_initiation = types.SimpleNamespace()
        temp_pre_initiation.team = team
        temp_pre_initiation.study_code = study_code
        temp_pre_initiation.pre_research_name = pre_research_name
        temp_pre_initiation.study_explanation = study_explanation
        temp_pre_initiation.type = type
        temp_pre_initiation.set_up = set_up
        temp_pre_initiation.PI = PI
        temp_pre_initiation.crc = crc
        temp_pre_initiation.is_withhold = is_withhold
        temp_pre_initiation.is_commence = is_commence
        temp_pre_initiation.tx = tx

        temp_pre_initiation.cancer = cancer
        temp_pre_initiation.phase = phase
        #temp_pre_initiation.chemotherapy = chemotherapy
        #temp_pre_initiation.alternation = alternation
        temp_pre_initiation.sponsor = sponsor
        temp_pre_initiation.CRO = CRO
        temp_pre_initiation.initiation_date = initiation_date
        temp_pre_initiation.CTC_contract = CTC_contract
        temp_pre_initiation.CTC_non_contract_reason = CTC_non_contract_reason
        temp_pre_initiation.memo = memo
        temp_pre_initiation.user = request.user

        return temp_pre_initiation, errors

    def __str__(self):
        return f'({self.pre_research_name}) {self.PI} {self.crc}'


class Pre_Initiation_SIT(models.Model):
    feasibility = models.DateField(blank=True, null=True)
    SIV = models.DateField(blank=True, null=True)
    PSV = models.DateTimeField(blank=True, null=True)
    budgeting_from = models.DateField(blank=True, null=True)
    budgeting_to = models.DateField(blank=True, null=True)
    IRB_new_review = models.DateField(blank=True, null=True)
    IRB_qualified_permission = models.DateField(blank=True, null=True)
    IRB_finalization = models.DateField(blank=True, null=True)
    contract = models.DateField(blank=True, null=True)
    # meta
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # relations
    pre_initiation = models.ForeignKey(Pre_Initiation, on_delete=models.SET_NULL, null=True, blank=True)

    @staticmethod
    def SIT_setup_form_validation(request, pre_initiation):
        errors = collections.defaultdict(list)

        # Get field values
        feasibility_str = request.POST.get('feasibility', '')
        SIV_str = request.POST.get('SIV', '')
        PSV_str = request.POST.get('PSV', '')
        budgeting_from_str = request.POST.get('budgeting_from', '')
        budgeting_to_str = request.POST.get('budgeting_to', '')
        IRB_new_review_str = request.POST.get('IRB_new_review', '')
        IRB_qualified_permission_str = request.POST.get('IRB_qualified_permission', '')
        IRB_finalization_str = request.POST.get('IRB_finalization', '')
        contract_str = request.POST.get('contract', '')

        try:
            feasibility = datetime.strptime(feasibility_str, '%m/%d/%Y')
        except:
            feasibility = None
        try:
            SIV = datetime.strptime(SIV_str, '%m/%d/%Y')
        except:
            SIV = None
        try:
            PSV = datetime.strptime(PSV_str, '%Y/%m/%d %H:%M')
        except:
            PSV = None
        try:
            budgeting_from = datetime.strptime(budgeting_from_str, '%m/%d/%Y')
        except:
            budgeting_from = None
        try:
            budgeting_to = datetime.strptime(budgeting_to_str, '%m/%d/%Y')
        except:
            budgeting_to = None
        try:
            IRB_new_review = datetime.strptime(IRB_new_review_str, '%m/%d/%Y')
        except:
            IRB_new_review = None
        try:
            IRB_qualified_permission = datetime.strptime(IRB_qualified_permission_str, '%m/%d/%Y')
        except:
            IRB_qualified_permission = None
        try:
            IRB_finalization = datetime.strptime(IRB_finalization_str, '%m/%d/%Y')
        except:
            IRB_finalization = None
        try:
            contract = datetime.strptime(contract_str, '%m/%d/%Y')
        except:
            contract = None

        temp_pre_initiation_SIT = types.SimpleNamespace()
        temp_pre_initiation_SIT.feasibility = feasibility
        temp_pre_initiation_SIT.SIV = SIV
        temp_pre_initiation_SIT.PSV = PSV
        temp_pre_initiation_SIT.budgeting_from = budgeting_from
        temp_pre_initiation_SIT.budgeting_to = budgeting_to
        temp_pre_initiation_SIT.IRB_new_review = IRB_new_review
        temp_pre_initiation_SIT.IRB_qualified_permission = IRB_qualified_permission
        temp_pre_initiation_SIT.IRB_finalization = IRB_finalization
        temp_pre_initiation_SIT.contract = contract
        temp_pre_initiation_SIT.uploader = request.user
        temp_pre_initiation_SIT.pre_initiation = pre_initiation

        return temp_pre_initiation_SIT, errors

    def __str__(self):
        return f'{self.pre_initiation}'


class Preperation(ResearchFieldModel):
    PLAN = 'plan'
    RESEARCH_TEAM = 'research_team'
    RESEARCH_FUNDS = 'research_funds'
    CHOICES = (
        (PLAN, "계획서"),
        (RESEARCH_TEAM, '연구진'),
        (RESEARCH_FUNDS, '연구비')
    )

class MFDS(ResearchFieldModel):
    NEW_RECEPTION = 'new_reception'
    QNA = 'qna'
    AMENDMENT = 'amendment'
    CHOICES = (
        (NEW_RECEPTION, "신규접수"),
        (QNA, '질의답변'),
        (AMENDMENT, '계획변경'),
    )

class IRB(ResearchFieldModel):
    NEW_RECEPTION = 'new_reception'
    QNA = 'qna'
    AMENDMENT = 'amendment'
    INTERIM_REPORT = 'interim_report'
    CHOICES = (
        (NEW_RECEPTION, "신규접수"),
        (QNA, '질의답변'),
        (AMENDMENT, '계획변경'),
        (INTERIM_REPORT, '중간보고'),
    )

class CRMS(ResearchFieldModel):
    CONTRACT_REVIEW = 'contract_review'
    DRUG_COST = 'drug_cost'
    DRUG_COST_REDUCTION = 'drug_cost_reduction'
    CTC_FUNDS = 'CTC_funds'
    CTC_AGREEMENT_APPLICATION = 'CTC_agreement_application'
    ALLOWANCE_OF_MEDICALCARE = 'allowance_of_medicalcare'
    ANTICANCER_ALLOWANCE_OF_MEDICALCARE = 'anticancer_allowance_of_medicalcare'
    GOV = 'GOV'
    CHOICES = (
        (CONTRACT_REVIEW, '계약 검토'),
        (DRUG_COST, '약제관리비 산정'),
        (DRUG_COST_REDUCTION, '약제관리비 감액신청'),
        (CTC_FUNDS, "CTC 비용산정"),
        (CTC_AGREEMENT_APPLICATION, 'CTC 협약신청'),
        (ALLOWANCE_OF_MEDICALCARE, '요양급여'),
        (ANTICANCER_ALLOWANCE_OF_MEDICALCARE, '항암요양급여'),
        (GOV, "GOV"),
    )

class MultiCenter(ResearchFieldModel):
    INITIAL_CONTRACT = 'initial_contract'
    CHANGE_CONTRACT = 'change_contract'
    ALLOWANCE_OF_MEDICALCARE_AND_CRIS = 'allowance_of_medicalcare_and_CRIS'
    OTHER_INSTITUTION_IRB = 'other_institution_irb'
    IP_DELIVERY = 'IP_delivery'
    TISSUE_BLOOD = 'tissue_blood'
    CHOICES = (
        (INITIAL_CONTRACT, "초기계약"),
        (CHANGE_CONTRACT, '변경계약'),
        (ALLOWANCE_OF_MEDICALCARE_AND_CRIS, '요양급여, CRIS'),
        (OTHER_INSTITUTION_IRB, "타기관 IRB"),
        (IP_DELIVERY, 'IP delivery'),
        (TISSUE_BLOOD, "물품 관련"),
    )

class Etc(ResearchFieldModel):
    RESEARCH_FUNDS = 'research_funds'
    PHARMACY_MANUAL = 'pharmacy_manual'
    LABEL = 'label'
    INSURANCE = 'insurance'
    SAE_REPORTING = 'SAE_reporting'
    CUSTOMS_CLEARANCE = 'customs_clearance'
    CRF = 'CRF'
    BINDER = 'binder'
    CHOICES = (
        (RESEARCH_FUNDS, "연구비 계산"),
        (PHARMACY_MANUAL, 'Pharmacy manual 제작'),
        (LABEL, '라벨 제작'),
        (INSURANCE, "보험"),
        (SAE_REPORTING, "SAE 보고 논의"),
        (CUSTOMS_CLEARANCE, '통관'),
        (CRF, 'CRF 제작 논의'),
        (BINDER, "바인더 제작"),
    )

class Pre_Initiation_IIT(models.Model):
    preperation = models.ForeignKey(Preperation, on_delete=models.SET_NULL, null=True)
    mfds = models.ForeignKey(MFDS, on_delete=models.SET_NULL, null=True, related_name='MFDS')
    irb = models.ForeignKey(IRB, on_delete=models.SET_NULL, null=True, related_name='IRB')
    crms = models.ForeignKey(CRMS, on_delete=models.SET_NULL, null=True)
    multicenter = models.ForeignKey(MultiCenter, on_delete=models.SET_NULL, null=True)
    etc = models.ForeignKey(Etc, on_delete=models.SET_NULL, null=True)
    from_date = models.DateField(blank=True, null=True)
    to_date = models.DateField(blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    # meta
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # relations
    pre_initiation = models.ForeignKey(Pre_Initiation, on_delete=models.SET_NULL, null=True, blank=True)

    @staticmethod
    def create_field_value_and_text():
        m2m_field_list = [Preperation, MFDS, IRB, CRMS, MultiCenter, Etc]
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
    def IIT_setup_form_validation(request, pre_initiation):
        errors = collections.defaultdict(list)

        # Get field values
        preperation_type = request.POST.get('preperation')
        preperation = Preperation.objects.filter(value=preperation_type).first()
        preperation_count = Preperation.objects.filter(value=preperation_type).count()
        mfds_type = request.POST.get('mfds')
        mfds = MFDS.objects.filter(value=mfds_type).first()
        mfds_count = MFDS.objects.filter(value=mfds_type).count()
        irb_type = request.POST.get('irb')
        irb = IRB.objects.filter(value=irb_type).first()
        irb_count = IRB.objects.filter(value=irb_type).count()
        crms_type = request.POST.get('crms')
        crms = CRMS.objects.filter(value=crms_type).first()
        crms_count = CRMS.objects.filter(value=crms_type).count()
        multicenter_type = request.POST.get('multicenter')
        multicenter = MultiCenter.objects.filter(value=multicenter_type).first()
        multicenter_count = MultiCenter.objects.filter(value=multicenter_type).count()
        etc_type = request.POST.get('etc')
        etc = Etc.objects.filter(value=etc_type).first()
        etc_count = Etc.objects.filter(value=etc_type).count()
        from_date_str = request.POST.get('from_date', '')
        to_date_str = request.POST.get('to_date', '')
        memo = request.POST.get('memo')

        try:
            from_date = datetime.strptime(from_date_str, '%m/%d/%Y')
        except:
            from_date = None
        try:
            to_date = datetime.strptime(to_date_str, '%m/%d/%Y')
        except:
            to_date = None

        if preperation_count + mfds_count + irb_count + crms_count + multicenter_count + etc_count != 1:
            errors['preperation'].append('- 1가지 항목만 선택 가능합니다.')
            errors['mfds'].append('')
            errors['irb'].append('')
            errors['crms'].append('')
            errors['multicenter'].append('')
            errors['etc'].append('')

        if preperation_count + mfds_count + irb_count + crms_count + multicenter_count + etc_count == 1 and not from_date:
            errors['from_date'].append('시작일을 입력하세요.')

        if preperation_type in Pre_Initiation_IIT.objects.filter(pre_initiation=pre_initiation, preperation__isnull=False).values_list('preperation__value', flat=True):
            errors['preperation'].append('이미 추가된 항목으로, 해당 항목의 날짜를 클릭하여 수정해 주시길 바랍니다.')
        elif mfds_type in Pre_Initiation_IIT.objects.filter(pre_initiation=pre_initiation, mfds__isnull=False).values_list('mfds__value', flat=True):
            errors['mfds'].append('이미 추가된 항목으로, 해당 항목의 날짜를 클릭하여 수정해 주시길 바랍니다.')
        elif irb_type in Pre_Initiation_IIT.objects.filter(pre_initiation=pre_initiation, irb__isnull=False).values_list('irb__value', flat=True):
            errors['irb'].append('이미 추가된 항목으로, 해당 항목의 날짜를 클릭하여 수정해 주시길 바랍니다.')
        elif crms_type in Pre_Initiation_IIT.objects.filter(pre_initiation=pre_initiation, crms__isnull=False).values_list('crms__value', flat=True):
            errors['crms'].append('이미 추가된 항목으로, 해당 항목의 날짜를 클릭하여 수정해 주시길 바랍니다.')
        elif multicenter_type in Pre_Initiation_IIT.objects.filter(pre_initiation=pre_initiation, multicenter__isnull=False).values_list('multicenter__value', flat=True):
            errors['multicenter'].append('이미 추가된 항목으로, 해당 항목의 날짜를 클릭하여 수정해 주시길 바랍니다.')
        elif etc_type in Pre_Initiation_IIT.objects.filter(Q(pre_initiation=pre_initiation, etc__isnull=False) & ~Q(etc__value='etc')).values_list('etc__value', flat=True):
            errors['etc'].append('이미 추가된 항목으로, 해당 항목의 날짜를 클릭하여 수정해 주시길 바랍니다.')

        temp_pre_initiation_IIT = types.SimpleNamespace()
        temp_pre_initiation_IIT.preperation = preperation
        temp_pre_initiation_IIT.mfds = mfds
        temp_pre_initiation_IIT.irb = irb
        temp_pre_initiation_IIT.crms = crms
        temp_pre_initiation_IIT.multicenter = multicenter
        temp_pre_initiation_IIT.etc = etc
        temp_pre_initiation_IIT.from_date = from_date
        temp_pre_initiation_IIT.to_date = to_date
        temp_pre_initiation_IIT.memo = memo
        temp_pre_initiation_IIT.uploader = request.user
        temp_pre_initiation_IIT.pre_initiation = pre_initiation

        return temp_pre_initiation_IIT, errors

    def __str__(self):
        return f'{self.pre_initiation}'

class End_research(models.Model):
    research_name = models.CharField(max_length=500, null=True)
    study_code = models.CharField(max_length=500, null=True)
    PI = models.CharField(max_length=500, null=True)
    status = models.CharField(choices=STATUS_CHOICES, null=True, max_length=50)
    binder_location = models.CharField(max_length=500, null=True)
    study_coordinator = models.CharField(max_length=500, null=True)
    storage_date = models.DateField(blank=True, null=True)
    end_brief = models.DateField(blank=True, null=True)
    result_brief = models.DateField(blank=True, null=True)
    sponsor = models.CharField(max_length=200, null=True)
    CRA_name = models.CharField(max_length=200, null=True)
    CRA_phoneNumber = models.CharField(max_length=200, null=True)

    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    @staticmethod
    def end_research_form_validation(request):
        errors = collections.defaultdict(list)

        # Get field values
        research_name = request.POST.get('research_name', None)
        study_code = request.POST.get('study_code', None)
        PI = request.POST.get('PI', None)
        status = request.POST.get('status', None)
        binder_location = request.POST.get('binder_location', None)
        study_coordinator = request.POST.get('study_coordinator', None)
        storage_date_str = request.POST.get('storage_date', '')
        end_brief_str = request.POST.get('end_brief', '')
        result_brief_str = request.POST.get('result_brief', '')
        sponsor = request.POST.get('sponsor', None)
        CRA_name= request.POST.get('CRA_name', None)
        CRA_phoneNumber = request.POST.get('CRA_phoneNumber', None)

        try:
            storage_date = datetime.strptime(storage_date_str, '%m/%d/%Y')
        except:
            storage_date = None
        try:
            end_brief = datetime.strptime(end_brief_str, '%m/%d/%Y')
        except:
            end_brief = None
        try:
            result_brief = datetime.strptime(result_brief_str, '%m/%d/%Y')
        except:
            result_brief = None

        if not research_name:
            errors['research_name'].append('- 연구명을 입력하세요.')
        if not status:
            errors['status'].append('- Status를 선택하세요.')

        temp_end_research = types.SimpleNamespace()
        temp_end_research.research_name = research_name
        temp_end_research.study_code = study_code
        temp_end_research.PI = PI
        temp_end_research.status = status
        temp_end_research.binder_location = binder_location
        temp_end_research.study_coordinator = study_coordinator
        temp_end_research.storage_date = storage_date
        temp_end_research.end_brief = end_brief
        temp_end_research.result_brief = result_brief
        temp_end_research.sponsor = sponsor
        temp_end_research.CRA_name = CRA_name
        temp_end_research.CRA_phoneNumber = CRA_phoneNumber

        return temp_end_research, errors

    def __str__(self):
        return self.research_name

def end_research_binder_image_directory_path(instance, filename):
    return 'binder_image/end_research/{0}/{1}'.format(instance.end_research.id, filename)

class End_UploadImage(models.Model): # 종료 보고 이후 연구 - 바인더 위치 (이미지)
    is_deleted = models.BooleanField(default=False)
    end_research = models.ForeignKey(End_research, on_delete=models.CASCADE)
    imagename = models.CharField(max_length=800)
    image = models.ImageField(upload_to=end_research_binder_image_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.image.url,
            'end_research': self.end_resaerch.id,
            'imagename': self.imagename
        }

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f'{self.end_research} -> {self.imagename}'


def end_research_archive_directory_path(instance, filename):
    return 'archive/end_research/{0}/{1}'.format(instance.end_research.id, filename)

class End_Research_Archive(models.Model): # 종료 보고 이후 연구 - 장기 보관 문서
    is_deleted = models.BooleanField(default=False)
    end_research = models.ForeignKey(End_research, on_delete=models.CASCADE)
    filename = models.CharField(max_length=800)
    file = models.FileField(upload_to=end_research_archive_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.file.url,
            'end_research': self.end_research.id,
            'filename': self.filename
        }


def research_archive_directory_path(instance, filename):
    return 'archive/research/{0}/{1}'.format(instance.research.id, filename)

class Research_Archive(models.Model): # 장기 보관 문서
    is_deleted = models.BooleanField(default=False)
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    filename = models.CharField(max_length=800)
    file = models.FileField(upload_to=research_archive_directory_path)

    def json(self):
        return {
            'id': self.id,
            'url': self.file.url,
            'research': self.research.id,
            'filename': self.filename
        }


class Study_Category(models.Model):
    name = models.CharField(max_length=100)


class Study_SubCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Study_Category, on_delete=models.CASCADE, related_name='study_subcategory')


class Study_Memo(models.Model):
    memo = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    sub_category = models.ForeignKey(Study_SubCategory, on_delete=models.CASCADE, related_name='study_memo')
    pre_initiation = models.ForeignKey(Pre_Initiation, on_delete=models.CASCADE, related_name='study_memo')


class DownloadLog(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)
    downloader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
