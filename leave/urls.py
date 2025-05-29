from django.urls import path
from . import views

app_name = 'leave'
urlpatterns = [
    path('calendar/', views.leave_calendar, name='leave_calendar'),
    path('add_event/', views.update, name='add_event'),
    path('edit/<int:leave_id>/', views.update, name='update'),
    path('delete/<int:leave_id>/', views.remove, name='remove'),
    path('all_events', views.all_events, name='all_events'),
    path('detail/<int:leave_id>/', views.leave_detail, name='leave_detail'),
    path('total_usage/', views.total_usage, name='total_usage'),

    # Patient Calendar
    path('patient/calendar/', views.patient_calendar, name='patient_calendar'),
    path('patient/all_events', views.patient_all_events, name='patient_all_events'),
    path('event/new/', views.event_update, name='event_update'),                           # /leave/patient/new
    path('event/edit/<int:patient_id>/', views.event_update, name='patient_edit'),             # /leave/patient/edit/{}
    path('patient/delete/<int:patient_id>/', views.patient_delete, name='patient_delete'),   # /leave/patient/delete/{}
]
