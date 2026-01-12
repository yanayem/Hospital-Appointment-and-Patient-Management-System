from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from datetime import date


# ---------------- LOGIN & SIGNUP ----------------
def LogInSignUppage(request):

    # ✅ next handling (GET + POST + SESSION)
    next_url = (
        request.POST.get("next")
        or request.GET.get("next")
        or request.session.get("next_url")
    )

    # ✅ store next in session on GET
    if request.method == "GET" and request.GET.get("next"):
        request.session["next_url"] = request.GET.get("next")

    if request.method == "POST":

        # -------- LOGIN --------
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
                request.session["user_id"] = user.id
                request.session["user_type"] = user.user_type
                request.session["current_role"] = user.user_type

                # 🔁 AUTO ROLE SWITCH
                if next_url:
                    if user.user_type == "doctor" and next_url.startswith("/patients/"):
                        request.session["current_role"] = "patient"

                    request.session.pop("next_url", None)
                    return redirect(next_url)

                return redirect(
                    "doctor_dashboard"
                    if user.user_type == "doctor"
                    else "patient_dashboard"
                )

            messages.error(request, "Invalid email or password!")


        #-----------------------
        # SIGNUP
        #----------------------

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


#======================

# ---------------- ROLE SWITCH ----------------
#===============================

def switch_to_patient(request):
    user = get_session_user(request)
    if user and user.user_type == "doctor":
        request.session["current_role"] = "patient"
        messages.success(request, "You are now using Patient Portal")
    return redirect("patient_dashboard")


def back_to_doctor(request):
    user = get_session_user(request)
    if user and user.user_type == "doctor":
        request.session["current_role"] = "doctor"
        messages.success(request, "Switched back to Doctor Portal 🩺")
    return redirect("doctor_dashboard")

# ---------------- LOGOUT ----------------
def logoutUser(request):
    for key in ["user_id", "user_type", "current_role"]:
        request.session.pop(key, None)
    return redirect("LogInSignUppage") 