from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'dataroom'
urlpatterns = [
    path('data/', views.searchdata, name='searchdata'),  # 해당 암종 자료실
    path('det/<int:research_id>/', views.detData, name='DataDet'),

    path('certification/', views.certification, name='certification'),  # 기기 Certi
    path('certification/create', views.create_certification, name='create_certification'),  # Certi 추가
    path('certification/delete', views.delete_certification, name='delete_category'),
    path('certification/download', views.download_certification, name='download_certification'),  # Certi 다운로드 이력
    path('certification/category/create', views.create_certification_category, name='create_certification_category'),

    path('good_clinical_practice/', views.good_clinical_practice, name='good_clinical_practice'),  # GCP
    path('good_clinical_practice/create', views.create_good_clinical_practice, name='create_good_clinical_practice'),  # GCP 추가
    path('good_clinical_practice/delete', views.delete_good_clinical_practice, name='delete_good_clinical_practice'),
    path('good_clinical_practice/download', views.download_good_clinical_practice, name='download_good_clinical_practice'),  # GCP 다운로드 이력
    path('good_clinical_practice/category/create', views.create_good_clinical_practice_category, name='create_good_clinical_practice_category'),

    path('crc/all_events', views.all_events, name='all_events'),
    path('crc/check_list/', views.crc_check_list, name='crc_check_list'),  # 교육일정
    path('crc/training/add/', views.training, name='training_new'),  # /crc/training/add
    path('crc/training/edit/<int:id>/', views.training, name='training_edit'),  # /crc/training/edit/{}
    path('crc/training/delete/<int:id>/', views.training_delete, name='training_delete'),  # /crc/training/delete/{}
    path('educational_material/', views.educational_material, name='educational_material'), # 교육자료
    path('educational_material/create', views.create_educational_material, name='create_educational_material'),
    path('educational_material/delete', views.delete_educational_material, name='delete_educational_material'),
    path('educational_material/download', views.download_educational_material, name='download_educational_material'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
