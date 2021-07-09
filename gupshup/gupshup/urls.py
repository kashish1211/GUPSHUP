"""gupshup URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
# from . import users
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
import notifications.urls
admin.site.site_header = 'Gupshup Admin Panel'
admin.site.site_title = 'Gupshup'
handler404 = 'users.views.handler404'
handler500 = 'users.views.handler500'

# handler404 = 'GUPSHUP.views.error_404'
# handler500 = 'GUPSHUP.views.error_500'
# handler403 = 'GUPSHUP.views.error_403'
# handler400 = 'GUPSHUP.views.error_400'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',user_views.register, name='register'),
    path('profile/',user_views.profile, name='profile'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('profile-registration/',user_views.profilereg,  name='profile-registration'),
    path('verification/', include('verify_email.urls')),
    # path('accounts/', include('allauth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    path('verify/', user_views.verify,name='verify'),	
    path('', include('blog.urls')),
    path('chat/', include('chat.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
