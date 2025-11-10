from django.contrib import admin
from django.urls import path, include  # include import korte hobe
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public Pages
    path('', views.homepage, name='homepage'),
    path('about-us/', views.aboutpage, name='AboutUs'),
    path('doctorinfo/', views.doctorpage, name='DoctorInfo'),
    path('services/', views.servicespage, name='ServicesPage'),path("ambulance/", views.ambulance_service_page, name="ambulance_page"),

    # Accounts (Login / Signup / Dashboard)
    path('patients/', include('patients.urls')),
    path('accounts/', include('accounts.urls')),
    path('doctors/', include('doctors.urls')),

    #path('patients/', include('patients.urls')),
    #path('doctors/', include('doctors.urls')),  
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)