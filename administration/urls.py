from django.urls import path
from . import views

app_name = 'administration'
urlpatterns = [
    path('organization/', views.organization),
    path('organization/delete/', views.organization_delete),

    path('user/', views.user),
    path('user/group/', views.user_group),
    path('user/group/delete/', views.user_group_delete),
    path('user/team/', views.user_team),
    path('user/team/delete/', views.user_team_delete),
    path('user/location/', views.user_location),
    path('user/location/delete/', views.user_location_delete),

    path('company/', views.company),
    path('company/delete/', views.company_delete),

    path('study_set_up/', views.study_set_up),
    path('study_set_up/delete/', views.study_set_up_delete),
    path('study_set_up/<int:study_category_id>/', views.study_set_up_subcategory),
    path('study_set_up/subcategory/delete/', views.study_set_up_subcategory_delete),

    path('cancer_image_set_up/', views.cancer_image_set_up),
    path('cancer_image_set_up/delete/', views.cancer_image_set_up_delete),
    path('cancer_image_set_up/image_links/', views.cancer_image_set_up_image_links),
    path('cancer_image_set_up/image_links/delete/', views.cancer_image_set_up_image_links_delete),
    path('cancer_image_set_up/images/', views.cancer_image_set_up_images),
    path('cancer_image_set_up/images/delete/', views.cancer_image_set_up_images_delete),

    path('notice/', views.notice),
    path('notice/delete/', views.notice_delete),

    path('commute/', views.commute),
    path('commute/download/excel', views.download_commute_excel),
    path('commute/download/pdf', views.download_commute_pdf),
]
