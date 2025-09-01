from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Job,Resume,Screening
from .serializers import RegistrationSerializer, JobSerializer, ResumeSerializer, ScreenerSerializer
from .utils import extract_text_from_pdf, extract_text_from_docx, extract_name, extract_skills, extract_email, extract_phone, calculate_similarity
import torch

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

    def perform_create(self, serializer):
        resume_file = self.request.FILES.get('uploaded_file')
        instance: Resume = serializer.save()   # type hint for PyCharm

        # Determine file type
        if resume_file and resume_file.name.lower().endswith('.pdf'):
            text = extract_text_from_pdf(instance.uploaded_file.path)
        elif resume_file and resume_file.name.lower().endswith('.docx'):
            text = extract_text_from_docx(instance.uploaded_file.path)
        else:
            text = ""

        # Extract structured info (with fallbacks to avoid IntegrityError)
        instance.parsed_text = text or "Not Found"
        instance.candidate_name = extract_name(text) or "Unknown"
        instance.email = extract_email(text) or "unknown@example.com"
        skills = extract_skills(text)
        instance.parsed_skills = ", ".join(skills) if skills else "Not Found"

        instance.save()

        # AI Matching & Scoring
        job_id = self.request.data.get('job_id')
        if job_id:
            try:
                job = Job.objects.get(id=job_id)
                score = calculate_similarity(instance.parsed_text, job.description)
                status = "shortlisted" if score >= 0.7 else "pending"

                Screening.objects.create(
                    job=job,
                    resume=instance,
                    score=score,
                    status=status
                )

            except Job.DoesNotExist:
                print(f"Job with id {job_id} does not exist")
            except Exception as e:
                print("Error creating screening:", e)

# Screening View
class ScreeningListView(generics.ListAPIView):
    queryset = Screening.objects.all()
    serializer_class = ScreenerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Screening.objects.all()
        job_id = self.request.query_params.get("job_id")  # ?job_id=1
        if job_id:
            queryset = queryset.filter(job_id=job_id)
        return queryset