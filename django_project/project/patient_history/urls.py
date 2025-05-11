from django.urls import path
from .views import login_view, signup_view, logout_view, doctor_dashboard, patient_dashboard, receptionist_dashboard,add_patient_details,add_doctor_details,update_profile,delete_profile, update_patient_profile, delete_patient_profile,add_prescription, view_prescription,view_details,manage_profile,manage_prescription,patient_view_prescription,add_appointment,manage_appointments,update_appointment,delete_appointment,show_appointments,patient_show_appointment,doctor_show_appointments

urlpatterns = [
    path('', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('add_patient_details/', add_patient_details, name='add_patient_details'),
    path('logout/', logout_view, name='logout'),
    path('doctor_dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('patient_dashboard/', patient_dashboard, name='patient_dashboard'),
    path('receptionist_dashboard/', receptionist_dashboard, name='receptionist_dashboard'),
    path('add_doctor_details/', add_doctor_details, name='add_doctor_details'),
    path('update_profile/', update_profile, name='update_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('update_patient_profile/', update_patient_profile, name='update_patient_profile'),
    path('delete_patient_profile/', delete_patient_profile, name='delete_patient_profile'),
    path('add_prescription/', add_prescription, name='add_prescription'),
    path('view_prescription/', view_prescription, name='view_prescription'),
    path('view_details/', view_details, name='view_details'),
    path('manage_profile/', manage_profile, name='manage_profile'),
    path('manage_prescription/', manage_prescription, name='manage_prescription'),
    path('patient_view_prescription/', patient_view_prescription, name='patient_view_prescription'),
    path('add_appointment/', add_appointment, name="add_appointment"),
    path("manage_appointments/", manage_appointments, name="manage_appointments"),
    path("update_appointment/<int:appointment_id>/", update_appointment, name="update_appointment"),
    path("delete_appointment/<int:appointment_id>/", delete_appointment, name="delete_appointment"),
    path('show_appointments/', show_appointments, name='show_appointments'),
     path('patient_show_appointments/', patient_show_appointment, name='patient_show_appointment'),
     path('doctor_show_appointments/', doctor_show_appointments, name='doctor_show_appointments'),
]


