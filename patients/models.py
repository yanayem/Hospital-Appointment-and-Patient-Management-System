# patients/models.py
from django.db import models
from accounts.models import UserProfile
from django.utils import timezone
from doctors.models import Appointment


class PatientProfile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="patient_profile")
    
    # Basic Info
    gender = models.CharField(max_length=10, blank=True, null=True)
    blood_group = models.CharField(max_length=3, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Optional details
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(upload_to="patient_profiles/", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Patient Profile: {self.user.name}"




class HealthRecord(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="health_records")
    doctor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="doctor_records")
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Record of {self.patient.name} by {self.doctor.name if self.doctor else 'Unknown'}"

from django.db import models
from accounts.models import UserProfile

class Prescription(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescribed_by')
    diagnosis = models.TextField()
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.name} by {self.doctor.name if self.doctor else 'N/A'} on {self.date}"



#=========================
# patients/models.py
from django.db import models
from accounts.models import UserProfile

class Notification(models.Model):
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.patient.name}"


