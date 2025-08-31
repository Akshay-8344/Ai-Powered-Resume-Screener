from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .models import Job,Resume,Screening
from .serializers import RegistrationSerializer, JobSerializer, ResumeSerializer, ScreenerSerializer


# Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

# Jobs create and list
class JobListCreateView(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

# Resume create and view
class ResumeUploadView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = [IsAuthenticated]

# Screening View
class ScreeningListView(generics.ListAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreenerSerializer
    permission_classes = [IsAuthenticated]




