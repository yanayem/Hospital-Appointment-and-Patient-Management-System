from django.urls import path
from . import views

urlpatterns = [
    path("", views.LogInSignUppage, name="LogInSignUppage"),
    path("logout/", views.logoutUser, name="logout"),
    path("switch-to-patient/", views.switch_to_patient, name="switch_to_patient"),
    path("back-to-doctor/", views.back_to_doctor, name="back_to_doctor"),
]
