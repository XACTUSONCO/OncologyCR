from django.urls import path
from . import views

app_name = 'miscellaneous'
urlpatterns = [
    path('vendor/download/<research_id>/', views.download_vendor),
    path('vendor/<int:research_id>/edit/', views.edit_vendor),

    # Supporting List
    path('supporting/add/', views.add_supporting, name='supporting'),
    path('supporting/add/<int:id>/', views.add_new_supporting, name='add_supporting'),
    path('supporting/delete_technician/', views.delete_technician, name='delete_technician'),
    path('supporting/update_technician/', views.update_technician, name='update_technician'),
    path('supporting/', views.supporting),
    path('supporting/<int:id>/edit/', views.edit_supporting, name='edit_supporting'),
    path('supporting/<int:id>/delete/', views.delete_supporting, name='delete_supporting'),
    path('supporting/delete_objects/', views.delete_objects, name='delete_objects'),
    path('supporting/download/', views.download_supporting),

    # 전체임상환자명단 Calendar 및 Download excel file
    path('this_week_patient_list/', views.CalendarView.as_view(), name='this_week_patient_list'),
    path('download_this_week_patient_list/', views.download_this_week_patient_list, name='download_this_week_patient_list'),

    # ID='94' study -> Naseron IV delivery
    path('94/add_delivery/', views.add_delivery, name='add_delivery'),
    path('94/<int:id>/edit_delivery/', views.edit_delivery, name='edit_delivery'),
    path('94/<int:id>/delete_delivery/', views.delete_delivery, name='delete_delivery'),
    path('94/update_checked/', views.update_checked, name='update_checked'),
    path('94/delete_checked/', views.delete_checked, name='delete_checked'),
    path('94/download/', views.download_IV_delivery),

    # Vendor에 따른 Query 관리
    path('QC/', views.QC_index, name='QC'),
    path('QC/add/', views.add_QC, name='add_QC'),
    path('QC/<int:id>/edit/', views.edit_QC, name='edit_QC'),
    path('QC/<int:id>/delete/', views.delete_QC, name='delete_QC'),
]
