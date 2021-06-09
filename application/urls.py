from django.contrib.auth import login
from . import views
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls.static import static

app_name='application'

urlpatterns = [
    path('api/auth/login/',views.AuthViewSet.as_view({'get': 'retrieve'}),name='login'),
    path('api/auth/logout/',views.AuthViewSet.as_view({'get': 'retrieve'}),name='logout'),
    path('api/auth/register/',views.Registration.as_view(),name='register')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)