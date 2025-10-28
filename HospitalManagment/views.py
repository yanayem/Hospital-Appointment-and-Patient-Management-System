# views.py
from django.shortcuts import render

def homepage(request):
    return render(request, 'home.html')  # home.html should be in templates folder
def aboutpage(request):
    return render(request, 'about.html')  # home.html should be in templates folder

def doctorpage(request):
    return render(request, 'doctor.html')  # home.html should be in templates folder
  
def servicespage(request):
    return render(request, 'services.html')

def appointmentpage(request):
    return render(request, 'appointment.html')
def LogInSignUppage(request):
    return render(request, 'log_sign.html')

