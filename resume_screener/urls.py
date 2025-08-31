from tkinter.font import names
from django.contrib import admin
from django.urls import path, include
from core.views import RegisterView, JobListCreateView, ResumeUploadView, ScreeningListView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/',RegisterView.as_view(), name='register'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('api/jobs/', JobListCreateView.as_view(), name='jobs'),
    path('api/resumes/', ResumeUploadView.as_view(), name='resumes'),
    path('api/screenings/', ScreeningListView.as_view(), name='screenings')
]

