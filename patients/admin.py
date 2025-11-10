from django.contrib import admin
from .models import PatientProfile, HealthRecord, Prescription, Notification


# ==========================
# PATIENT PROFILE ADMIN
# ==========================
@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "blood_group", "age", "phone", "created_at")
    search_fields = ("user__name", "user__email", "phone", "blood_group")
    list_filter = ("gender", "blood_group", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)


# ==========================
# HEALTH RECORD ADMIN
# ==========================
@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "diagnosis", "date")
    search_fields = ("patient__name", "doctor__name", "diagnosis")
    list_filter = ("date",)
    ordering = ("-date",)
    readonly_fields = ("date",)


# ==========================
# PRESCRIPTION ADMIN
# ==========================
@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "diagnosis", "date")
    search_fields = ("patient__name", "doctor__name", "diagnosis", "treatment")
    list_filter = ("date",)
    ordering = ("-date",)
    readonly_fields = ("date",)


# ==========================
# NOTIFICATION ADMIN
# ==========================
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "patient", "created_at", "is_read")
    search_fields = ("title", "message", "patient__name")
    list_filter = ("is_read", "created_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
