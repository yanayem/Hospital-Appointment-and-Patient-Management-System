from django.urls import path
from .views import (
    login_signup, logoutUser, doctor_dashboard, patient_dashboard, 
    switch_to_patient, back_to_doctor
)

urlpatterns = [
    path("", login_signup, name="LogInSignUppage"),
    path("logout/", logoutUser, name="logout"),
    path("doctor/", doctor_dashboard, name="doctor_dashboard"),
    path("patient/", patient_dashboard, name="patient_dashboard"),
    path("switch-to-patient/", switch_to_patient, name="switch_to_patient"),
    path("back-to-doctor/", back_to_doctor, name="back_to_doctor"),
]
