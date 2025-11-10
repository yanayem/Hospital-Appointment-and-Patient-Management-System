from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile


# ---------------- LOGIN & SIGNUP ----------------
def login_signup(request):
    if request.method == "POST":

        # LOGIN
        if "login" in request.POST:
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = None
            try:
                found_user = UserProfile.objects.get(email=email)
                if found_user.check_password(password):
                    user = found_user
            except UserProfile.DoesNotExist:
                pass

            if user:
                # store user info in session
                request.session["user_id"] = user.id
                request.session["user_type"] = user.user_type
                request.session["current_role"] = user.user_type  # for switching

                if user.user_type == "doctor":
                    return redirect("doctor_dashboard")
                else:
                    return redirect("patient_dashboard")
            else:
                messages.error(request, "Invalid email or password!")

        # SIGNUP
        elif "signup" in request.POST:
            user_type = request.POST.get("user_type")
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            password = request.POST.get("password")
            confirm = request.POST.get("confirm_password")

            if password != confirm:
                messages.error(request, "Passwords do not match")
            elif UserProfile.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                user = UserProfile.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    user_type=user_type,
                    name=name,
                    phone=phone,
                )

                # extra info
                if user_type == "patient":
                    user.age = request.POST.get("age")
                    user.address = request.POST.get("address")
                elif user_type == "doctor":
                    user.specialization = request.POST.get("specialization")
                    user.license = request.POST.get("license")

                user.save()
                messages.success(request, "Account created successfully! Please log in.")

    return render(request, "login_signup.html")


# ---------------- HELPER ----------------
def get_session_user(request):
    """Helper to get logged-in user from session"""
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    try:
        user = UserProfile.objects.get(id=user_id)
        # Override user_type for role-switching
        current_role = request.session.get("current_role")
        if current_role and current_role in ["doctor", "patient"]:
            user.current_role = current_role
        else:
            user.current_role = user.user_type
        return user
    except UserProfile.DoesNotExist:
        return None

from datetime import date
# ---------------- DASHBOARDS ----------------
def doctor_dashboard(request):
    user = get_session_user(request)
    if not user:
        return redirect("login_signup")

    if user.user_type != "doctor":
        return redirect("patient_dashboard")

    # Prevent doctor acting as patient mode
    if request.session.get("current_role") == "patient":
        return redirect("patient_dashboard")

    return render(request, "doctor_dashboard.html", {"user": user})

#======================


#===============================

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


# ---------------- ROLE SWITCH ----------------
def switch_to_patient(request):
    user = get_session_user(request)
    if user:
        # ✅ doctor হলে, role switch করে patient করবো
        if user.user_type == "doctor":
            request.session["current_role"] = "patient"
            request.session["user_type"] = "patient"  # ← গুরুত্বপূর্ণ
            messages.success(request, "You are now using the Patient Portal 💖")
        else:
            messages.info(request, "You are already a patient.")
    return redirect("patient_dashboard")


def back_to_doctor(request):
    user = get_session_user(request)
    if user:
        # ✅ শুধুমাত্র doctor হলে আবার doctor role restore করবো
        if user.user_type == "doctor":
            request.session["current_role"] = "doctor"
            request.session["user_type"] = "doctor"  # ← গুরুত্বপূর্ণ
            messages.success(request, "Switched back to Doctor Portal 🩺")
        else:
            messages.info(request, "You are not a doctor account.")
    return redirect("doctor_dashboard")


# ---------------- LOGOUT ----------------
def logoutUser(request):
    for key in ["user_id", "user_type", "current_role"]:
        request.session.pop(key, None)
    return redirect("LogInSignUppage")  # ✅ fixed redirect name
