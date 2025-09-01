from django.core.validators import validate_email
from rest_framework import serializers
from .models import Job, Resume, Screening
from django.contrib.auth.models import User


#registration
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email = validated_data.get('email'),
            password = validated_data['password']
        )
        return user


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


class ScreenerSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    resume = ResumeSerializer()
    class Meta:
        model = Screening
        fields = '__all__'

