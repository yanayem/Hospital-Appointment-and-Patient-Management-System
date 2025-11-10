from django.shortcuts import render
# from django.contrib.auth.models import User  # remove
# from .models import UserProfile  # remove
from accounts.models import UserProfile

# ------------------------- PUBLIC PAGES -------------------------
def homepage(request):
    return render(request, 'home.html')

def aboutpage(request):
    return render(request, 'about.html')

from django.shortcuts import render
from doctors.models import DoctorProfile  # ✅ import model from doctors app

def doctorpage(request):
    doctors = DoctorProfile.objects.select_related("user").all()
    return render(request, "doctor.html", {"doctors": doctors})


def servicespage(request):
    return render(request, 'services.html')

from django.shortcuts import render

# 🌸 Ambulance Service Page (demo data)
def ambulance_service_page(request):
    # Demo data list (can later be replaced with a model)
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
        {
            "name": "LifeLine Express",
            "service_type": "Advanced Life Support",
            "location": "Banani, Dhaka",
            "price": 80,
            "status": "Available",
            "phone": "01798765432",
            "image": "img/ambulance2.jpg",
        },
        {
            "name": "RapidRescue",
            "service_type": "Patient Transport Service",
            "location": "Mirpur, Dhaka",
            "price": 40,
            "status": "Busy",
            "phone": "01812398765",
            "image": "img/ambulance3.jpg",
        },
    ]

    return render(request, "ambulance_services.html", {"ambulances": ambulances})
