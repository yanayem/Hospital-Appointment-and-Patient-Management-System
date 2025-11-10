from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('appointments/<int:appointment_id>/update/', views.update_appointment_status, name='update_appointment_status'),
    path('patients/', views.doctor_patients, name='doctor_patients'),
    path("patients/<int:patient_id>/history/", views.patient_history, name="patient_history"),
    path('addnotes/', views.doctor_addnotes, name='doctor_addnotes'),
    path("notes/delete/<int:note_id>/", views.delete_note, name="delete_note"),
    path('notifications/', views.doctor_notifications, name='doctor_notifications'),
    path('profile/', views.doctor_profile, name='doctor_profile'),

    # ❌ Remove this line because no such view exists
     path("health-records/", views.doctor_health_records, name="doctor_health_records"),

   # path("prescriptions/", views.doctor_prescriptions, name="doctor_prescriptions"),

    # ✅ Correct health record routes
    path('patient/<int:patient_id>/records/', views.view_health_records, name='view_health_records'),
    path('patient/<int:patient_id>/add-record/', views.add_or_edit_health_record, name='add_health_record'),
    path('patient/<int:patient_id>/edit-record/<int:record_id>/', views.add_or_edit_health_record, name='edit_health_record'),
    path('delete-record/<int:record_id>/', views.delete_health_record, name='delete_health_record'),
    path('profile/delete-pic/', views.delete_doctor_pic, name='delete_doctor_pic'),
]
