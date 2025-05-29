from feedback import views
from django.urls import path

app_name = 'feedback'
urlpatterns = [
    # 환자 및 연구 검색
    path('feedback/search/', views.search),
    # 피드백 관련 URL (feedback)
    path('feedback/<int:feedback_id>/edit/', views.edit_feedback),
    path('feedback/<int:feedback_id>/delete/', views.delete_feedback),
    # 환자 배정 관련 URL (assignment)
    path('assignment/<int:assignment_id>/', views.detail_assignment),
    path('assignment/<int:assignment_id>/new_feedback/', views.add_feedback),
    path('assignment/<int:assignment_id>/edit/', views.edit_assignment),
    path('assignment/<int:assignment_id>/delete/', views.delete_assignment),

    path('assignment/upload/', views.assignment_upload),
    path('feedback/upload/', views.feedback_upload)
]