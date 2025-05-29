from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .utils import rename_imagefile_to_uuid
from django.urls import reverse
from user.models import User
import os
from django.utils import timezone

CANCER_CHOICES = [
    ('Breast', 'Breast'),
    ('Stomach', 'Stomach'),
    ('Sarcoma', 'Sarcoma'),
    ('CRC', 'CRC'),
    ('Urological', 'Urological'),
    ('Lung', 'Lung'),
    ('Melanoma', 'Melanoma'),
    ('Phase1', 'Phase1'),
    ('Pancreatic', 'Pancreatic')]

TRAINING_OR_CERTIFICATE_CHOICES = [
    ('Training', 'Training'),
    ('15A', '15A 병동'),
    ('CTC', 'CTC'),
    ('병리과', '병리과'),
    ('심전도_폐기능', '심전도, 폐기능'),
    ('안과', '안과'),
    ('암병원_채혈실', '암병원 채혈실'),
    ('영상의학과', '영상의학과'),
    ('종양내과_외래', '종양내과 외래'),
    ('초음파', '초음파'),
    ('항암주사실', '항암주사실'),
    ('온도기록지', '온도기록지(-70도 냉동고)'),
    ('A팀관리기기', 'A팀 관리기기')]

LANGUAGE_CHOICES = [
    ('korean', '국문'),
    ('english', '영문')
]
LANGUAGE_CHOICES_INV = {val: val for val, _ in LANGUAGE_CHOICES}


class Image(models.Model):  # 임상 연구 정보 포함
    research = models.ForeignKey('research.Research', on_delete=models.CASCADE, blank=True, null=True)
    m_name = models.CharField(max_length=50, default="")
    m_scr = models.CharField(max_length=50, default="")
    m_ongo = models.CharField(max_length=50, default="")
    m_enroll = models.CharField(max_length=50, default="")
    m_target = models.CharField(max_length=50, default="")

    cancer = models.CharField(max_length=50, choices=CANCER_CHOICES, default="")
    slide_number = models.IntegerField(null=False, default="1")

    def __str__(self):
        return f'{self.m_name} -> research: {self.research} | {self.cancer} | {self.slide_number}'


class Image_link(models.Model): # 각 임상 연구에 대한 (scr/ongo/enroll/target/waiting) + detail button
    clinical_trial = models.ForeignKey(Image, on_delete=models.SET_NULL, default='', null=True, blank=True)
    link_top = models.CharField(null=True, max_length=10)
    link_left = models.CharField(null=True, max_length=10)
    link_right = models.CharField(null=True, max_length=10)
    link_bottom = models.CharField(null=True, max_length=10)

    def __str__(self):
        return str(self.clinical_trial)


class Page(models.Model):  # ppt 슬라이드 이미지 포함
    cancer = models.CharField(max_length=50, choices=CANCER_CHOICES, default="")
    slide_number = models.IntegerField(null=False, default="1")
    slide = models.ImageField(upload_to='images/')

    # slide = models.CharField(max_length=500, null=True)

    def delete(self, *args, **kwargs):
        self.slide.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.cancer) + ' | ' + str(self.slide_number) + ' | ' + str(self.slide)


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


class protocol_upload(models.Model):
    clinical_trial = models.ForeignKey('research.Research', on_delete=models.SET_NULL, blank=True, null=True)
    protocol_file_ko = models.FileField(upload_to='protocol_ko/', null=True, blank=True)
    protocol_file_eng = models.FileField(upload_to='protocol_eng/', null=True, blank=True)

    inclusion = models.ImageField(upload_to='criteria/inclusion/', null=True, blank=True)
    exclusion = models.ImageField(upload_to='criteria/exclusion/', null=True, blank=True)
    reference = models.ImageField(upload_to=rename_imagefile_to_uuid, storage=OverwriteStorage(), null=True, blank=True)

    def __str__(self):
        return str(self.clinical_trial)


# CRC 교육 일정
class training_schedule(models.Model):
    topic = models.CharField(blank=True, max_length=500)
    trainer = models.CharField(blank=True, max_length=100)
    date = models.DateTimeField(null=True)
    location = models.CharField(blank=True, max_length=100)
    memo = models.TextField(blank=True, null=False)
    is_deleted = models.BooleanField(default=False)

    def get_time(self):
        return timezone.localtime(self.date).strftime('%H:%M')

    @property
    def get_html_url(self):
        url = reverse('dataroom:training_edit', args=(self.id,))
        return f'<div class="training-title" data-toggle="modal" data-target="#training_{self.id}"><div style="font-weight:bold;">{self.get_time()}</div>' \
               f'<div style="word-wrap:break-word;">{self.topic}</div>' \
               f'<a href="{url}" style="color:black;">&nbsp;&nbsp;<span style="color:red;">Edit</span></a></div>'

    def __str__(self):
        return str(self.topic)


# CRC 교육 자료
class Material(models.Model):
    category = models.CharField(max_length=50, default="")
    name = models.CharField(blank=True, max_length=500)  # 기기명
    asset_number = models.CharField(blank=True, null=True, max_length=100)  # 자산번호
    year = models.IntegerField(blank=True, null=True)  # 년도
    materials = models.FileField(upload_to='certification_materials/', blank=True, null=True)
    materials_name = models.CharField(blank=True, max_length=500)
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @staticmethod
    def get_categories():
        return MaterialCategory.objects.filter(is_deleted=0).values_list('category', flat=True).distinct().order_by('category')

    def __str__(self):
        return str(self.category) + ' | ' + str(self.name) + ' | ' + str(self.materials)


class MaterialCategory(models.Model):
    category = models.CharField(max_length=50, default="")
    description = models.CharField(blank=True, max_length=500)
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    link = "Edit"


class MaterialDownload(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    downloader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


class Educational_Material(models.Model):
    category = models.CharField(max_length=50, default="")
    name = models.CharField(blank=True, max_length=500)
    version = models.CharField(blank=True, max_length=50)
    materials = models.FileField(upload_to='educational_materials/', blank=True, null=True)
    materials_name = models.CharField(blank=True, max_length=500)
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.category) + ' | ' + str(self.name) + ' | ' + str(self.materials)


class Educational_Material_Download(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    educational_material = models.ForeignKey(Educational_Material, on_delete=models.SET_NULL, null=True, blank=True)
    downloader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    

# GCP
class GCPMaterialCategory(models.Model):
    category = models.CharField(max_length=50, default="")
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)


def GCP_directory_path(instance, filename):
    return 'GCP/{0}/{1}/{2}'.format(instance.category, instance.year, filename)


class GCPMaterial(models.Model):
    category = models.CharField(max_length=50, default="")
    name = models.CharField(blank=True, max_length=500)  # 연구자
    year = models.IntegerField(blank=False)
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, blank=True, null=True)
    materials = models.FileField(upload_to=GCP_directory_path, blank=True, null=True)
    materials_name = models.CharField(blank=True, max_length=500)
    is_deleted = models.BooleanField(default=False)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    uploader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @staticmethod
    def get_categories():
        return GCPMaterialCategory.objects.filter(is_deleted=0).values_list('category', flat=True).distinct().order_by('id')

    @staticmethod
    def field_value_and_text():
        ret = {
            'language': LANGUAGE_CHOICES
        }
        return ret

    def __str__(self):
        return str(self.category) + ' | ' + str(self.name) + ' | ' + str(self.materials)


class GCPMaterialDownload(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    material = models.ForeignKey(GCPMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    downloader = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
