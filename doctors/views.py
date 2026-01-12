# doctors/views.py
#==================================================
#  IMPORTS
#==================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now, localtime
from django.db.models import Q
from django.http import JsonResponse
from accounts.models import UserProfile
from .models import DoctorProfile, Appointment, DoctorNote, DoctorNotification
from django.utils import timezone
from patients.models import Notification
from django.views.decorators.http import require_POST
from datetime import date, datetime, timedelta
from patients.models import HealthRecord
from .models import Appointment
from django.contrib import messages
import os
from django.utils.timezone import localdate
import pytz

# ===================================================
#  HELPERS
# ===================================================

def get_session_user(request):
    """Return logged-in doctor from session."""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    try:
        return UserProfile.objects.get(id=user_id, user_type="doctor")
    except UserProfile.DoesNotExist:
        return None

# ===================================================
#  LOGIN REQUIRED DECORATOR
# ===================================================

def login_required_view(func):
    """Decorator for session-based doctor login"""
    def wrapper(request, *args, **kwargs):
        user = get_session_user(request)
        if not user:
            messages.warning(request, "Please login as a doctor first 🩺")
            return redirect("LogInSignUppage")
        return func(request, *args, **kwargs)
    return wrapper


# ===================================================
#  DOCTOR DASHBOARD
# ===================================================

@login_required_view
def doctor_dashboard(request):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    # -----------------------------
    #  Dhaka timezone today
    # -----------------------------
    dhaka_tz = pytz.timezone("Asia/Dhaka")
    now_dhaka = datetime.now(dhaka_tz)
    today_dhaka = now_dhaka.date()

    # -----------------------------
    #  TODAY appointments
    # -----------------------------
    todays_appointments = Appointment.objects.filter(
        doctor=doctor,
        date=today_dhaka
    ).order_by("time")

    # -----------------------------
    #  UPCOMING appointments (tomorrow onwards)
    # -----------------------------
    upcoming_appointments = Appointment.objects.filter(
        doctor=doctor,
        date__gt=today_dhaka,
        status__in=["Pending", "Confirmed"]
    ).order_by("date", "time")

    context = {
        "doctor": doctor,
        "today": today_dhaka,
        "todays_appointments": todays_appointments,
        "upcoming_appointments": upcoming_appointments,
    }

    return render(request, "doctor_dashboard.html", context)

# ===================================================
#  APPOINTMENTS
# ===================================================

@login_required_view
def doctor_appointments(request):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    today = date.today()
    now = datetime.now()

    # ✅ All appointments for this doctor
    appointments = Appointment.objects.filter(doctor=doctor).order_by("date", "time")

    # ✅ Split logic:
    todays_appointments = []
    upcoming_appointments = []
    previous_appointments = []

    for appt in appointments:
        appt_datetime = datetime.combine(appt.date, appt.time)

        if appt.date == today and appt_datetime >= now:
            # still today but not yet happened
            todays_appointments.append(appt)
        elif appt_datetime > now:
            # future
            upcoming_appointments.append(appt)
        else:
            # ✅ past appointments (automatically mark as completed if not already)
            if appt.status not in ["Completed", "Cancelled"]:
                appt.status = "Completed"
                appt.save()
            previous_appointments.append(appt)

    # ✅ Auto remove appointments older than 1 day
    cutoff = today - timedelta(days=1)
    Appointment.objects.filter(date__lt=cutoff).delete()

    context = {
        "doctor": doctor,
        "todays_appointments": todays_appointments,
        "upcoming_appointments": upcoming_appointments,
        "previous_appointments": previous_appointments,
    }
    return render(request, "appointments.html", context)

#--------------------------------------------------
# Update appointment status (AJAX or normal POST)
#--------------------------------------------------

@require_POST
@login_required_view
def update_appointment_status(request, appointment_id):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    try:
        appointment = Appointment.objects.get(id=appointment_id, doctor=doctor)
    except Appointment.DoesNotExist:
        return JsonResponse({"success": False, "error": "Appointment not found"}, status=404)

    new_status = request.POST.get("status")
    if not new_status:
        return JsonResponse({"success": False, "error": "Invalid status"}, status=400)

    appointment.status = new_status
    appointment.save()

    # Doctor notification
    DoctorNotification.objects.create(
        doctor=doctor,
        message=f"Appointment with {appointment.patient.name} was marked as {new_status}."
    )

    # Patient notification
    Notification.objects.create(
        patient=appointment.patient,
        title=f"Appointment {new_status}",
        message=f"Your appointment with Dr. {doctor.name} on {appointment.date} at {appointment.time} is now {new_status}."
    )

    # AJAX response
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"success": True, "status": new_status, "id": appointment.id})

    messages.success(request, f"Appointment marked as {new_status}")
    return redirect("doctor_appointments")

#--------------------------------------------------
# Confirm an appointment
#--------------------------------------------------

@login_required_view
def confirm_appointment(request, id):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    appointment = get_object_or_404(Appointment, id=id, doctor=doctor)

    appointment.status = "Confirmed"
    appointment.save()

    # Doctor's own notification
    DoctorNotification.objects.create(
        doctor=doctor,
        message=f"You confirmed an appointment with {appointment.patient.name} on {appointment.date} at {appointment.time}."
    )

    # Patient notification
    Notification.objects.create(
        patient=appointment.patient,
        title="Appointment Confirmed 💖",
        message=f"Your appointment with Dr. {doctor.name} on {appointment.date} at {appointment.time} has been confirmed."
    )

    messages.success(request, f"Appointment confirmed with {appointment.patient.name} ✅")
    return redirect("doctor_appointments")

# ===================================================
# PATIENT LIST & HISTORY
# ===================================================

@login_required_view
def doctor_patients(request):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    appointments = Appointment.objects.filter(
        doctor=doctor, status__in=["Confirmed", "Completed"]
    ).select_related("patient")

    patient_ids = appointments.values_list("patient_id", flat=True).distinct()
    patients = UserProfile.objects.filter(id__in=patient_ids)

    return render(request, "doctor_patients.html", {"patients": patients, "doctor": doctor})

#--------------------------------------------------
# Patient History Details
#--------------------------------------------------

@login_required_view
def patient_history(request, patient_id):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    patient = get_object_or_404(UserProfile, id=patient_id)
    appointments = Appointment.objects.filter(doctor=doctor, patient=patient).order_by("-date", "-time")

    return render(request, "doctor_patient_history.html", {
        "patient": patient,
        "appointments": appointments,
        "doctor": doctor,
    })


# ===================================================
#  NOTES
# ===================================================

@login_required_view
def doctor_addnotes(request):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    patient_ids = Appointment.objects.filter(
        doctor=doctor, status__in=["Confirmed", "Completed"]
    ).values_list("patient", flat=True).distinct()
    patients = UserProfile.objects.filter(id__in=patient_ids)

    note_to_edit = None
    if edit_id := request.GET.get("edit"):
        note_to_edit = get_object_or_404(DoctorNote, id=edit_id, doctor=doctor)

    if request.method == "POST":
        note_id = request.POST.get("note_id")
        patient_id = request.POST.get("patient")
        note_text = request.POST.get("note")

        if not patient_id or not note_text:
            messages.error(request, "Please select a patient and write a note.")
        else:
            patient = get_object_or_404(UserProfile, id=patient_id)
            if note_id:
                note = get_object_or_404(DoctorNote, id=note_id, doctor=doctor)
                note.note = note_text
                note.patient = patient
                note.save()
                messages.success(request, "Note updated successfully ✏️")
            else:
                DoctorNote.objects.create(doctor=doctor, patient=patient, note=note_text)
                messages.success(request, f"Note added for {patient.name} 🩺")
            return redirect("doctor_addnotes")

    notes = DoctorNote.objects.filter(doctor=doctor).select_related("patient").order_by("-created_at")

    context = {
        "doctor": doctor,
        "patients": patients, 
        "notes": notes, 
        "note_to_edit": note_to_edit}
    return render(request, "doctor_addnotes.html", context)

#------------------------------------------
# 🗑️ Delete a note
#------------------------------------------

@login_required_view
def delete_note(request, note_id):
    doctor = get_session_user(request)
    note = get_object_or_404(DoctorNote, id=note_id, doctor=doctor)
    note.delete()
    messages.success(request, "Note deleted successfully 🗑️")
    return redirect("doctor_addnotes")


# ===================================================
# 🔔  NOTIFICATIONS
# ===================================================

@login_required_view
def doctor_notifications(request):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    notifications = DoctorNotification.objects.filter(doctor=doctor).distinct().order_by("-created_at")
    unread_count = notifications.filter(is_read=False).count()

    # Mark all unread as read
    DoctorNotification.objects.filter(doctor=doctor, is_read=False).update(is_read=True)

    return render(request, "doctor_notifications.html", {
        "notifications": notifications,
        "doctor": doctor,
        "unread_count": unread_count,
    })

#============================
#Add health record
#============================

@login_required_view
def doctor_health_records(request):
    doctor = get_session_user(request)  # ✅ current logged-in doctor

    if not doctor:
        messages.warning(request, "Please login as a doctor first 🩺")
        return redirect("LogInSignUppage")

    # ✅ Only show patients who have Confirmed OR Completed appointments
    confirmed_appointments = Appointment.objects.filter(
        doctor=doctor,
        status__in=["Confirmed", "Completed"]  # ✅ allow both Confirmed & Completed
    )

    patient_ids = confirmed_appointments.values_list("patient__id", flat=True).distinct()
    patients = UserProfile.objects.filter(id__in=patient_ids, user_type__in=["patient", "doctor"])


    selected_patient = None
    records = None
    patient_id = request.GET.get("patient")

    if patient_id:
        selected_patient = get_object_or_404(UserProfile, id=patient_id, user_type__in=["patient", "doctor"])

        # ✅ Make sure the selected patient actually belongs to this doctor’s confirmed/completed list
        if selected_patient.id not in patient_ids:
            messages.error(request, "You don’t have permission to view this patient’s records ❌")
            return redirect("doctor_health_records")

        # ✅ Fetch health records for this doctor-patient pair
        records = HealthRecord.objects.filter(doctor=doctor, patient=selected_patient)

    context = {
        "doctor": doctor,
        "patients": patients,
        "selected_patient": selected_patient,
        "records": records,
    }
    return render(request, "doctor_health_records.html", context)

#------------------------------------------
# 🩺 List all records of a specific patient
#------------------------------------------

@login_required_view
def view_health_records(request, patient_id):
    return redirect(f"/doctors/health-records/?patient={patient_id}")


#------------------------------------------
# ➕ Add or Edit Health Record
#------------------------------------------

@login_required_view
def add_or_edit_health_record(request, patient_id, record_id=None):
    doctor = get_session_user(request)
    patient = get_object_or_404(UserProfile, id=patient_id, user_type__in=["patient", "doctor"])
    record = None

    if record_id:
        record = get_object_or_404(HealthRecord, id=record_id, doctor=doctor)

    if request.method == "POST":
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        notes = request.POST.get("notes")

        if record:
            # Update existing record
            record.diagnosis = diagnosis
            record.treatment = treatment
            record.notes = notes
            record.save()

            Notification.objects.create(
                patient=patient,
                title="Health Record Updated",
                message=f"Dr. {doctor.name} updated your health record.",
            )

            messages.success(request, "Health record updated successfully ✏️")
        else:
            # Create new record
            HealthRecord.objects.create(
                patient=patient,
                doctor=doctor,
                diagnosis=diagnosis,
                treatment=treatment,
                notes=notes,
            )

            Notification.objects.create(
                patient=patient,
                title="New Health Record Added",
                message=f"Dr. {doctor.name} added a new health record for you.",
            )

            messages.success(request, "Health record added successfully 🩺")

        return redirect("view_health_records", patient_id=patient.id)

    return render(request, "doctor_add_health_record.html", {
        "doctor": doctor,
        "patient": patient,
        "record": record
    })

#------------------------------------------
# Delete a health record 
#------------------------------------------

@login_required_view
def delete_health_record(request, record_id):
    doctor = get_session_user(request)
    record = get_object_or_404(HealthRecord, id=record_id, doctor=doctor)
    patient_id = record.patient.id
    record.delete()
    messages.success(request, "Health record deleted successfully 🗑️")
    return redirect("view_health_records", patient_id=patient_id)
#--------------------------------------------------------------------------------------------------


# ===================================================
#  DOCTOR PROFILE
# ===================================================

@login_required_view
def doctor_profile(request):
    doctor = get_session_user(request)
    if not doctor:
        return redirect("LogInSignUppage")

    profile, _ = DoctorProfile.objects.get_or_create(user=doctor)

    if request.method == "POST":
        if "profile_pic" in request.FILES:
            profile.profile_pic = request.FILES["profile_pic"]
            profile.save()
            messages.success(request, "Profile picture updated successfully 💖")
            return redirect("doctor_profile")

        # Update doctor basic info
        doctor.name = request.POST.get("name", doctor.name)
        doctor.phone = request.POST.get("phone", doctor.phone)
        doctor.email = request.POST.get("email", doctor.email)
        doctor.address = request.POST.get("address", doctor.address)
        doctor.gender = request.POST.get("gender", doctor.gender)
        doctor.visit_fee = request.POST.get("visit_fee", doctor.visit_fee)
        doctor.save()

        # Update extended profile info
        profile.specialization = request.POST.get("specialization", profile.specialization)
        profile.highest_qualification = request.POST.get("highest_qualification", profile.highest_qualification)
        profile.license = request.POST.get("license", profile.license)
        profile.experience_years = request.POST.get("experience_years", profile.experience_years)
        profile.expertise_areas = request.POST.get("expertise_areas", profile.expertise_areas)
        profile.specialized_treatments = request.POST.get("specialized_treatments", profile.specialized_treatments)
        profile.biography = request.POST.get("biography", profile.biography)
        profile.address = request.POST.get("address", profile.address)
        profile.save()

        messages.success(request, "Profile updated successfully 💕")
        return redirect("doctor_profile")

    context = {
        "doctor": doctor,
        "profile": profile,
        "genders": ["Male", "Female", "Other"],
    }
    return render(request, "doctor_profile.html", context)


#------------------------------
# Delete Doctor Profile Picture
#------------------------------

def delete_doctor_pic(request):
    if request.method == "POST":
        user = get_session_user(request)  # ✅ get the currently logged-in UserProfile
        
        try:
            doctor_profile = DoctorProfile.objects.get(user=user)
        except DoctorProfile.DoesNotExist:
            messages.error(request, "Doctor profile not found.")
            return redirect('doctor_profile')

        if doctor_profile.profile_pic:
            try:
                # Delete file from storage if it exists
                if doctor_profile.profile_pic and os.path.isfile(doctor_profile.profile_pic.path):
                    os.remove(doctor_profile.profile_pic.path)

                # Remove from model
                doctor_profile.profile_pic = None
                doctor_profile.save()

                messages.success(request, "✅ Profile picture deleted successfully.")
            except Exception as e:
                messages.error(request, f"⚠️ Error deleting profile picture: {e}")
        else:
            messages.warning(request, "⚠️ No profile picture found to delete.")

    return redirect('doctor_profile')

