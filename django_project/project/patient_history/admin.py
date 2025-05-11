from django.contrib import admin
from .models import Doctor, Patient, Prescription, Receptionist, Appointment

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Receptionist)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'appointment_date', 'appointment_time')
