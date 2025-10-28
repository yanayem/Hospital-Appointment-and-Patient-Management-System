from django.contrib import admin
from django.urls import path
from HospitalManagment import views  # <- absolute import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='homepage'),
    path('about-us/', views.aboutpage, name='AboutUs'),
    path('doctorinfo/', views.doctorpage, name='DoctorInfo'),
    path('services/', views.servicespage, name='ServicesPage'),
    path('appointment/', views.appointmentpage, name='AppointmentPage'),
    path('login/', views.LogInSignUppage, name='LogInSignUppage'),
]
