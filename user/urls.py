from django.urls import path

from . import views

urlpatterns = [
    path('term/', views.term),
    path('security/', views.security),
    path('', views.view_profile),
    path('edit/', views.edit_profile),
    path('list/', views.user_list),
    path('contact/edit/<int:id>/', views.edit_contact),
    path('contact/download/', views.download_contact),
    path('profile/overview/', views.profile_overview),
    path('profile/edit/info/', views.profile_edit_info),
    path('profile/edit/password/', views.edit_profile),
]
