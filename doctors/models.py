# doctors/models.py
from django.db import models
from django.utils import timezone
from accounts.models import UserProfile


class DoctorProfile(models.Model):
    gender = models.CharField(
    max_length=10,
    choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
    blank=True,
    null=True
    ) 
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=500, blank=True, null=True)
    highest_qualification = models.CharField(max_length=500, blank=True, null=True)
    license = models.CharField(max_length=100, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    expertise_areas = models.TextField(blank=True, null=True)
    specialized_treatments = models.TextField(blank=True, null=True)
    biography = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="doctor_profiles/", blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    visit_fee = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return f"Dr. {self.user.name}"


class Appointment(models.Model):
    doctor = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="appointments_by_doctor",
        limit_choices_to={'user_type': 'doctor'}
    )
    patient = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="appointments_by_patient",
        limit_choices_to={'user_type': 'patient'}
    )
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    service = models.CharField(max_length=100, blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'),
                 ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )

    def __str__(self):
        return f"Appointment: Dr. {self.doctor.name} with {self.patient.name}"


from django.db import models
from accounts.models import UserProfile
from django.utils import timezone

class DoctorNote(models.Model):
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="notes_by_doctor")
    patient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="notes_for_patient")
    note = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Note for {self.patient.name} by Dr. {self.doctor.name}"


from django.db import models
from accounts.models import UserProfile

class DoctorNotification(models.Model):
    doctor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="doctor_notifications")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.doctor.name} - {self.message[:30]}"
