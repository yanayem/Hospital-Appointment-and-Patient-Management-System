from django.contrib import admin
from .models import DoctorProfile, Appointment, DoctorNote, DoctorNotification

# ============================
# 👨‍⚕️ Doctor Profile Admin
# ============================
@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "specialization", "highest_qualification", "visit_fee", "experience_years")
    search_fields = ("user__name", "user__email", "specialization")
    list_filter = ("specialization", "experience_years")
    ordering = ("user__name",)
    list_per_page = 20


# ============================
# 📅 Appointment Admin
# ============================
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor", "patient", "date", "time", "status")
    search_fields = ("doctor__name", "patient__name", "service")
    list_filter = ("status", "date")
    ordering = ("-date", "-time")
    list_per_page = 25


# ============================
# 📝 Doctor Notes Admin
# ============================
@admin.register(DoctorNote)
class DoctorNoteAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor", "patient", "created_at")
    search_fields = ("doctor__name", "patient__name", "note")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    list_per_page = 20


# ============================
# 🔔 Doctor Notifications Admin
# ============================
@admin.register(DoctorNotification)
class DoctorNotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor", "message", "created_at", "is_read")
    search_fields = ("doctor__name", "message")
    list_filter = ("is_read", "created_at")
    ordering = ("-created_at",)
    list_per_page = 20
