"""oncology_abc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from oncology_abc import settings
import oncology_abc.views
import user.views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', oncology_abc.views.index),
    # feedback and assignment
    path('', include('feedback.urls')),
    path('admin/', admin.site.urls),
    path('research/', include('research.urls')),
    path('dataroom/', include('dataroom.urls')),
    path('user/', include('user.urls')),
    path('leave/', include('leave.urls')),
    path('miscellaneous/', include('miscellaneous.urls')),
    path('administration/', include('administration.urls')),
    path('login/', user.views.login_view),
    path('logout/', user.views.logout_view),
    path('register/', user.views.register),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
