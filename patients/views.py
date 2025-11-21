# patients/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from doctors.models import DoctorProfile
from accounts.models import UserProfile
from .models import (
    PatientProfile,
    Appointment,
    HealthRecord,
    Prescription,
    Notification
)

# ==========================
#   HELPERS
# ==========================

def get_session_user(request):
    """Return the currently logged-in user (doctor or patient mode)."""
    user_id = request.session.get("user_id")
    if not user_id:
        return None

    try:
        user = UserProfile.objects.get(id=user_id)
        mode = request.session.get("mode")

        # Force role view: if doctor in patient mode → act as patient
        if mode == "patient":
            user.user_type = "patient"
        return user
    except UserProfile.DoesNotExist:
        return None


def login_required_view(func):
    """Custom decorator for session-based login."""
    def wrapper(request, *args, **kwargs):
        user = get_session_user(request)
        if not user:
            messages.warning(request, "Please login first.")
            return redirect("LogInSignUppage")
        return func(request, *args, **kwargs)
    return wrapper


# ==========================
#   PATIENT PROFILE
# ==========================
@login_required_view
def patient_profile(request):
    """View and update patient profile"""
    patient = get_session_user(request)
    if not patient:
        return redirect("LogInSignUppage")

    # Always link to UserProfile (NOT username)
    profile, created = PatientProfile.objects.get_or_create(user=patient)

    if request.method == "POST":
        if 'profile_pic' in request.FILES:
            profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            messages.success(request, "Profile picture updated!")
            return redirect("patient_profile")
        else:
            # Save other info
            patient.name = request.POST.get("name", patient.name)
            patient.phone = request.POST.get("phone", patient.phone)
            patient.age = request.POST.get("age", patient.age)
            patient.gender = request.POST.get("gender", patient.gender)
            patient.save()
            profile.blood_group = request.POST.get("blood_group", profile.blood_group)
            profile.address = request.POST.get("address", profile.address)
            profile.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("patient_profile")

    context = {
        "patient": patient,
        "profile": profile,
        "blood_groups": ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
        "genders": ["Male", "Female", "Other"],
    }
    return render(request, "patient_profile.html", context)

# ==========================
#   PATIENT DASHBOARD
# ==========================


# ==========================
#   APPOINTMENTS
# ==========================

# ==========================
#   APPOINTMENTS
# ==========================
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import now
from doctors.models import DoctorProfile
from patients.models import Appointment, Notification
from accounts.views import get_session_user


@login_required_view
def book_appointment(request, doctor_id=None):
    """
    Book an appointment page.
    - If doctor_id is given, preselect that doctor.
    - Redirects to login if patient not logged in.
    """
    # Get patient from session
    patient = get_session_user(request)
    if not patient or patient.user_type != "patient":
        login_url = reverse("LogInSignUppage")
        return redirect(f"{login_url}?next={request.path}")

    # List of all doctors
    doctors = DoctorProfile.objects.all()

    # Preselect doctor if doctor_id is given
    selected_doctor = None
    if doctor_id:
        selected_doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    # Handle form submission
    if request.method == "POST":
        doctor_id_post = request.POST.get("doctor")
        service = request.POST.get("service")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        appointment_date = request.POST.get("date")
        appointment_time = request.POST.get("time")
        reason = request.POST.get("reason")

        if not all([doctor_id_post, service, email, phone, appointment_date, appointment_time]):
            messages.error(request, "Please fill in all required fields 💖")
            return redirect(request.path)  # redirect back to same page

        # Get DoctorProfile object
        doctor = get_object_or_404(DoctorProfile, id=doctor_id_post)

        # Create appointment
        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            service=service,
            email=email,
            phone=phone,
            date=appointment_date,
            time=appointment_time,
            reason=reason
        )

        # Create notification
        Notification.objects.create(
            patient=patient,
            title="Appointment Booked 💖",
            message=f"Your appointment with Dr. {doctor.user.name} on {appointment_date} at {appointment_time} has been booked successfully."
        )

        messages.success(request, f"Appointment booked with Dr. {doctor.user.name}! 💕")
        return redirect('my_appointments')

    context = {
        "patient": patient,
        "doctors": doctors,
        "selected_doctor": selected_doctor,
        "today": now().date()
    }

    return render(request, "book_appointment.html", context)

from datetime import date
@login_required_view
def my_appointments(request):
    patient = get_session_user(request)
    if not patient:
        return redirect("LogInSignUppage")

    today = date.today()
    todays_appointments = Appointment.objects.filter(patient=patient, date=today)
    upcoming_appointments = Appointment.objects.filter(patient=patient, date__gt=today)

    return render(request, "my_appointments.html", {
        "todays_appointments": todays_appointments,
        "upcoming_appointments": upcoming_appointments,
    })

@login_required_view
def edit_appointment(request, id):
    patient = get_session_user(request)
    appointment = get_object_or_404(Appointment, id=id, patient=patient)

    if request.method == 'POST':
        appointment.service = request.POST.get('service', appointment.service)
        appointment.email = request.POST.get('email', appointment.email)
        appointment.phone = request.POST.get('phone', appointment.phone)
        appointment.date = request.POST.get('date', appointment.date)
        appointment.time = request.POST.get('time', appointment.time)
        appointment.reason = request.POST.get('reason', appointment.reason)
        appointment.save()

        messages.success(request, f"Appointment with Dr. {appointment.doctor.name} updated 💖")
        return redirect('my_appointments')

    return render(request, 'edit_appointment.html', {'appointment': appointment})


@login_required_view
def cancel_appointment(request, id):
    patient = get_session_user(request)
    appointment = get_object_or_404(Appointment, id=id, patient=patient)

    if request.method == 'POST':

        Notification.objects.create(
        patient=patient,
        title="Appointment Cancelled 💔",
        message=f"Your appointment with Dr. {appointment.doctor.name} on {appointment.date} was cancelled."
        )
        
        appointment.delete()
        messages.success(request, f"Appointment with Dr. {appointment.doctor.name} cancelled 💔")
        return redirect('my_appointments')

    return render(request, 'cancel_appointment.html', {'appointment': appointment})


# ==========================
#   HEALTH RECORDS
# ==========================

@login_required_view
def health_records(request):
    patient = get_session_user(request)
    if not patient:
        messages.warning(request, "Please login first.")
        return redirect("LogInSignUppage")

    records = HealthRecord.objects.filter(patient=patient).order_by('-date')
    return render(request, "health_records.html", {"records": records, "patient": patient})


@login_required_view
def add_health_record(request):
    if request.method == "POST":
        patient_id = request.POST.get("patient_id")
        doctor_id = request.POST.get("doctor_id")
        diagnosis = request.POST.get("diagnosis")
        treatment = request.POST.get("treatment")
        notes = request.POST.get("notes")

        try:
            patient = UserProfile.objects.get(id=patient_id)
            doctor = UserProfile.objects.get(id=doctor_id) if doctor_id else None
        except UserProfile.DoesNotExist:
            messages.error(request, "Patient or Doctor not found.")
            return redirect("health_records")

        HealthRecord.objects.create(
            patient=patient,
            doctor=doctor,
            diagnosis=diagnosis,
            treatment=treatment,
            notes=notes
        )
        messages.success(request, "Health record added successfully 💖")
        return redirect("health_records")

    context = {
        "patients": UserProfile.objects.filter(user_type='patient'),
        "doctors": UserProfile.objects.filter(user_type='doctor')
    }
    return render(request, "add_health_record.html", context)


# ==========================
#   PRESCRIPTIONS
# ==========================

@login_required_view
def prescription_history(request):
    patient = get_session_user(request)
    if not patient:
        messages.warning(request, "Please login first.")
        return redirect("LogInSignUppage")

    prescriptions = Prescription.objects.filter(patient=patient).order_by('-date')
    return render(request, 'prescription_history.html', {"patient": patient, "prescriptions": prescriptions})


# ==========================
#   NOTIFICATIONS
# ==========================

@login_required_view
def notifications(request):
    patient = get_session_user(request)
    if not patient:
        messages.warning(request, "Please login first.")
        return redirect("LogInSignUppage")

    notifications = Notification.objects.filter(patient=patient).order_by('-created_at')
    return render(request, 'notifications.html', {"patient": patient, "notifications": notifications})



from django.shortcuts import redirect
from django.contrib import messages
from .models import PatientProfile

def delete_patient_pic(request):
    user = get_session_user(request)
    if not user:
        messages.error(request, "User not found.")
        return redirect('patient_profile')

    try:
        profile = PatientProfile.objects.get(user=user)
        if profile.profile_pic:
            profile.profile_pic.delete(save=True)
            profile.profile_pic = None
            profile.save()
            messages.success(request, "Profile picture deleted successfully.")
        else:
            messages.info(request, "No profile picture to delete.")
    except PatientProfile.DoesNotExist:
        messages.error(request, "Patient profile not found.")

    return redirect('patient_profile')


from django.shortcuts import render

def contact_support(request):
    return render(request, "contact_support.html")



#=========================================
#
#==========================================

from django.shortcuts import render, redirect
from datetime import date
from accounts.models import UserProfile
from patients.models import HealthRecord, Prescription, Notification
# Make sure Appointment model exists:
from patients.models import Appointment  

def patient_dashboard(request):
    user = get_session_user(request)
    if not user:
        return redirect("login_signup")

    # Allow doctor in patient mode
    is_doctor_as_patient = user.user_type == "doctor" and getattr(user, "current_role", None) == "patient"
    show_back_to_doctor = is_doctor_as_patient

    # ✅ Fetch related data
    health_records = HealthRecord.objects.filter(patient=user).order_by("-date")
    prescriptions = Prescription.objects.filter(patient=user).order_by("-date")
    notifications = Notification.objects.filter(patient=user).order_by("-created_at")

    # ✅ Appointment data (if model exists)
    today = date.today()

    today_appointments = Appointment.objects.filter(
        patient=user,
        date=today
    ).order_by("time")

    upcoming_appointments = Appointment.objects.filter(
        patient=user,
        date__gt=today
    ).order_by("date", "time")[:2]

    # ✅ Identify missing personal fields for “Profile Incomplete” message
    missing_fields = []
    for field in ["age", "address", "phone", "gender", "blood_group"]:
        if not getattr(user, field, None):
            missing_fields.append(field)

    # ✅ Context
    context = {
        "user": user,
        "patient": user,
        "show_back_to_doctor": show_back_to_doctor,
        "acting_as_patient": is_doctor_as_patient,
        "health_records": health_records,
        "prescriptions": prescriptions,
        "notifications": notifications,
        "missing_personal_fields": missing_fields,
        "today_appointments": today_appointments,
        "upcoming_appointments": upcoming_appointments,
    }

    return render(request, "patient_dashboard.html", context)
