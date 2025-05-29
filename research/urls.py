from django.conf.urls import url
from django.urls import path
from . import views
from .views import CrcListView

urlpatterns = [
    # path('', views.index),
    path('search/', views.search_research),
    path('search/download/', views.download_search),
    path('add/', views.add_research),
    path('<int:research_id>/', views.detail_research),
    path('<int:research_id>/download/', views.download_assignment),
    path('<int:research_id>/new_assignment/', views.new_assignment),
    path('<int:research_id>/update_assignment/<int:research_waitinglist_id>/', views.update_assignment),    # waitinglist -> new assignment
    path('<int:research_id>/update_pre_scr_assignment/<int:pre_scr_assignment_id>/', views.update_pre_scr_assignment),  # Pre screening -> new assignment
    path('<int:research_id>/delete/', views.delete_research),
    path('<int:research_id>/edit/', views.edit_research),
    path('<int:research_id>/update_target/', views.update_target), # onco_cr_count 객체 생성 및 수정
    path('delete_target/', views.delete_target), # onco_cr_count 객체 삭제

    path('CRC/list/', CrcListView.as_view()),
    path('CRC/list/ongoing/<str:crc>/', views.crc_ongoing_list),
    path('CRC/list/screening/<str:crc>/', views.crc_screening_list),
    path('CRC/list/input_gap/<str:crc>/', views.crc_input_gap_list),
    path('PI/list/', views.pi_research_list),
    path('CRC_statistic/', views.CRC_statistics),
    path('CRC_statistic/monthly_enroll/', views.monthly_enroll, name='monthly_enroll'),
    path('CRC_statistic/monthly_visit/', views.monthly_visit, name='monthly_visit'),
    path('PI_statistic/', views.PI_statistics),
    path('ETC_statistic/', views.ETC_statistics),
    path('not_entered_statistic/', views.not_entered_statistic),
    path('statistic/ongoing/download/', views.download_ongoing),
    path('statistic/performance/download/', views.download_performance),
    path('statistic/download/', views.download_statistics),

    # Pre Initiation Research List
    path('pre_initiation/update_research/<int:id>/', views.update_research),    # Pre-Initiation -> new research
    path('pre_initiation/', views.pre_initiation),   # 개시 연구 index page
    path('pre_initiation/add/', views.add_pre_initiation),
    path('pre_initiation/<int:id>/', views.detail_pre_initiation),
    path('pre_initiation/<int:id>/edit/', views.edit_pre_initiation),
    path('pre_initiation/<int:id>/delete/', views.delete_pre_initiation),
    # 개시연구 - SIT
    path('pre_initiation/SIT/<int:pre_initiation_id>/add_setup/', views.add_SIT_setup),
    path('pre_initiation/SIT/<int:setup_id>/edit/', views.edit_SIT_setup),
    path('pre_initiation/SIT/<int:setup_id>/delete/', views.delete_SIT_setup),
    # 개시연구 - IIT
    path('pre_initiation/IIT/<int:pre_initiation_id>/add_setup/', views.add_IIT_setup),
    path('pre_initiation/IIT/memo/', views.add_IIT_memo),
    path('pre_initiation/IIT/<int:setup_id>/edit/', views.edit_IIT_setup),
    path('pre_initiation/IIT/<int:setup_id>/delete/', views.delete_IIT_setup),

    # cancer별 Waiting List 관련 URL
    path('waitinglist/add/phase/2/', views.phase_add_waiting, name='phase_add_waiting'),
    path('waitinglist/add/<int:cancer_id>/', views.add_waiting, name='add_waiting'),
    path('waitinglist/<int:waitinglist_id>/', views.detail_waiting),
    path('waitinglist/<int:waitinglist_id>/edit/', views.edit_waiting),
    path('waitinglist/<int:waitinglist_id>/delete/', views.delete_waiting),
    path('waitinglist/add/PI/', views.add_waiting_PI, name='add_waiting_PI'),

    # research별 Waiting List 관련 URL
    path('waitinglist/add/research/<int:research_id>/', views.add_research_waiting, name='add_research_waiting'),
    path('waitinglist/research/<int:research_waitinglist_id>/edit/', views.edit_research_waiting),
    path('waitinglist/research/<int:research_waitinglist_id>/delete/', views.delete_research_waiting),

    # 종료 연구
    path('end_study/', views.end_study, name='end_study'),
    path('end_study/add/', views.add_end_research, name='add_end_research'),
    path('end_study/<int:id>/edit/', views.edit_end_research, name='edit_end_research'),
    path('end_study/<int:id>/delete/', views.delete_end_research, name='delete_end_research'),
    path('end_study/search/', views.search_end_study, name='search_end_study'),
]
