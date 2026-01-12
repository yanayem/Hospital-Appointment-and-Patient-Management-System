from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public pages
    path('', views.homepage, name='homepage'),
    path("contact-support/", views.contact_support, name="contact_support"),
    path('about-us/', views.aboutpage, name='AboutUs'),
    path('doctorinfo/', views.doctorpage, name='DoctorInfo'),
    path('services/', views.servicespage, name='ServicesPage'),
    path('ambulance/', views.ambulance_service_page, name='ambulance_page'),

    # Apps
    path('accounts/', include('accounts.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
