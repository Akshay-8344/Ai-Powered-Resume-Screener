from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import title


class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    required_skills = models.TextField()

    def __str__(self):
        return self.title


class Resume(models.Model):
    candidate_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True,null=True)
    uploaded_file = models.FileField(upload_to='media/resumes/')
    parsed_text = models.TextField(blank=True,null=True)
    parsed_skills = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.candidate_name if self.candidate_name else f"Resume {self.id}"


class Screening(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='screenings')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,related_name='screenings')
    score = models.FloatField(default=0.0)
    status = models.CharField(max_length=50, choices=[
        ("pending", "Pending"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    ], default="pending")

    def __str__(self):
        return f"{self.resume} - {self.job} ({self.score})"