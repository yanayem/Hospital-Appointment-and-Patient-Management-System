# patients/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage
from doctors.models import DoctorProfile

# ---------------- HOME ----------------
def homepage(request):
    return render(request, 'home.html')


# ---------------- CONTACT SUPPORT ----------------

def contact_support(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message_text = request.POST.get("message")

        # Save message
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )

        # Success message
        messages.success(request, "Your message has been sent successfully 💖")

        # Redirect back to homepage so messages show
        return redirect('homepage')

# ---------------- OTHER PAGES ----------------

def aboutpage(request):
    return render(request, 'about.html')

# ---------------- DOCTOR INFO PAGE ----------------

def doctorpage(request):
    doctors = DoctorProfile.objects.select_related("user").all()
    return render(request, "doctor.html", {"doctors": doctors})

# ---------------- SERVICES PAGE ----------------

def servicespage(request):
    return render(request, 'services.html')

# ---------------- AMBULANCE SERVICE PAGE ----------------

def ambulance_service_page(request):
    ambulances = [
        {
            "name": "CityCare Ambulance",
            "service_type": "Basic Life Support",
            "location": "Dhanmondi, Dhaka",
            "price": 50,
            "status": "Available",
            "phone": "01712345678",
            "image": "img/ambulance1.jpg",
        },
    ]
    return render(request, "ambulance_services.html", {"ambulances": ambulances})
