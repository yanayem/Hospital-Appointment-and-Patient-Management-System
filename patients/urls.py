from django.urls import path
from . import views
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
     path("dashboard/", views.patient_dashboard, name="patient_dashboard"),
    path('profile/', views.patient_profile, name='patient_profile'),
    path('profile/delete-pic/', views.delete_patient_pic, name='delete_patient_pic'),
    path('book/', views.book_appointment, name='book_appointment'),
    path("book-appointment/<int:doctor_id>/", views.book_appointment, name="book_appointment"),
    path('appointments/', views.my_appointments, name='my_appointments'),
    path('records/', views.health_records, name='health_records'),
    path('add_record/', views.add_health_record, name='add_health_record'),
    path('prescriptions/', views.prescription_history, name='prescription_history'),
    path('notifications/', views.notifications, name='notifications'),
    path('appointments/edit/<int:id>/', views.edit_appointment, name='edit_appointment'),
    path('appointments/cancel/<int:id>/', views.cancel_appointment, name='cancel_appointment'),
    path("contact-support/", views.contact_support, name="contact_support"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)