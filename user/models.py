from django.db import models
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
import collections, types
from datetime import datetime, date
from django.utils import timezone
from dateutil.relativedelta import relativedelta

LOCATION_CHOICES = [
    ('제중관 B1층', '제중관 B1층'),
    ('광혜관 B1층', '광혜관 B1층'),
    ('광혜관 B3층 (1)', '광혜관 B3층 (1)'),
    ('광혜관 B3층 (2)', '광혜관 B3층 (2)'),
    ('15A 병동 신약 모니터링실', '15A 병동 신약 모니터링실'),
    ('암병원 B5층', '암병원 B5층'),
    ('제중관 2층', '제중관 2층'),
]
LOCATION_CHOICES_INV = {val: val for val, _ in LOCATION_CHOICES}

TEAM_CHOICES = [
    ('CLUE', 'CLUE'),
    ('GSI', 'GSI'),
    ('etc', 'etc'),
]
TEAM_CHOICES_INV = {val: val for val, _ in TEAM_CHOICES}

# Create your models here.
class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.time, self.username)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.time, self.username)

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    AuditEntry.objects.create(action='user_logged_in', username=user.username)


#@receiver(user_logged_out) # 세션 만료 시간(60분)이 초과되면 logout 되어 user 정보를 가져올 수 없어 해당 기능 중지
#def user_logged_out_callback(sender, request, user, **kwargs):
#    AuditEntry.objects.create(action='user_logged_out', username=user.username)

class Team(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)


class Location(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)


class Contact(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    eng_name = models.CharField(max_length=50, blank=True, default='', null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    work_phone = models.CharField(max_length=50, blank=True, null=True)
    career = models.DateField(blank=True, null=True)
    career_end = models.DateField(blank=True, null=True)
    is_senior = models.BooleanField(default=False)
    onco_A = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def group_str(self):
        groups = Group.objects.filter(user=self.user)
        return ', '.join(map(str, groups))

    @property
    def career_period(self):
        """
            근무기간 'Y년 M개월' 형식으로 반환
        """
        if self.career is None:
            return None
        end_date = self.career_end or date.today()
        rd = relativedelta(end_date, self.career)
        return f"{rd.years}년 {rd.months}개월"

    def get_career_duration(self, reference_date=None):
        """
        (년, 개월) 튜플 반환 – 내부 계산용
        """
        if self.career is None:
            return None

        reference_date = reference_date or date.today()
        end_date = self.career_end or reference_date
        rd = relativedelta(end_date, self.career)

        years, months = rd.years, rd.months

        if self.user and self.user.id == 199:
            years += 1

        return years, months

    def get_fixed_annual(self, reference_date=None):
        duration = self.get_career_duration(reference_date)
        if duration is None:
            return 0
        years, months = duration
        if years == 0 and months == 0:
            return 0
        elif years == 0 and months <= 2:
            return 1
        elif years == 0 and months <= 5:
            return 2
        elif years == 0 and months <= 8:
            return 3
        elif years == 0 and months <= 12:
            return 4

        elif years == 1:
            return 8
        elif years == 2:
            return 10
        elif years == 3:
            return 12
        elif years >= 4:
            return 13

    def get_fixed_monthly(self, reference_date=None):
        """
        월차 개수 계산:
            - 1개월 미만: 0
            - 1년 미만 & 작년 12월 1일 이전 입사자: reference_date.month 개 부여
            - 1년 미만 & 작년 12월 1일 이후 입사자: 입사 후 꽉 찬 개월 수 계산
            - 1년 이상: 12
        """
        if self.career is None:
            return 0

        reference_date = reference_date or date.today()
        december = date(reference_date.year - 1, 12, 1)

        years, months = self.get_career_duration(reference_date)

        if years == 0 and months == 0:
            return 0

        # 1년 미만 + 12월 이전 입사자
        elif years == 0 and self.career < december:
            return reference_date.month

        # 1년 미만 + 12월 이후 입사자
        elif years == 0 and self.career >= december:
            rd = relativedelta(reference_date, self.career)
            return rd.years * 12 + rd.months

        # 1년 이상
        else:
            return 12

    @staticmethod
    def contact_form_validation(request):
        errors = collections.defaultdict(list)

        # Get field values
        name = request.POST.get('name')
        eng_name = request.POST.get('eng_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        work_phone = request.POST.get('work_phone')
        location = request.POST.get('location', '')
        #career_str = request.POST.get('career')
        #career_end_str = request.POST.get('career_end')
        team = request.POST.get('team', '')

        # convert to proper values
        try:
            location = Location.objects.filter(id=location).first()
        except:
            location = None
        try:
            team = Team.objects.filter(id=team).first()
        except:
            team = None

        temp_contact = types.SimpleNamespace()
        temp_contact.name = name
        temp_contact.eng_name = eng_name
        temp_contact.email = email
        temp_contact.phone = phone
        temp_contact.work_phone = work_phone
        temp_contact.location = location
        temp_contact.team = team
        temp_contact.user = request.user

        return temp_contact, errors

    def json(self):
        return {'id': self.id, 'type': self.name, 'show': self.name}

    CHOICES = tuple()
    INV_CHOICES = {}

    @property
    def inv_choices(self):
        m2m_field = [Contact]
        for c in m2m_field:
            #queryset = c.objects.filter(Q(onco_A=1) & ~Q(team__name='etc')).values('name')
            queryset = c.objects.values('name')
            choices = tuple((str(q['name']), str(q['name'])) for q in queryset)

            if not self.INV_CHOICES:
                self.INV_CHOICES = {value: text for value, text in choices}
            return self.INV_CHOICES

    # @receiver(post_save, sender=User)
    # def create_user_contact(sender, instance, created, **kwargs):
    #     if created:
    #         Contact.objects.create(user=instance)

    #@receiver(post_save, sender=User)
    #def save_user_contact(sender, instance, **kwargs):
    #    instance.contact.save()

    def __str__(self):
        return str(self.name)


class InvestigatorContact(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    onco_A = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Agreement(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    term_agreement_date = models.DateTimeField(blank=True, null=True)
    security_agreement_date = models.DateTimeField(blank=True, null=True)

    @staticmethod
    def set_term_agreement_date(self):
        now = timezone.now()
        self.term_agreement_date = now
        AgreementLog(user=self.user, term_agreement_date=now).save()
        self.save()

    @staticmethod
    def set_security_agreement_date(self):
        now = timezone.now()
        self.security_agreement_date = now
        AgreementLog(user=self.user, security_agreement_date=now).save()
        self.save()


class AgreementLog(models.Model):
    term_agreement_date = models.DateTimeField(blank=True, null=True)
    security_agreement_date = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
