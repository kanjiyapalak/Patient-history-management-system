from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import date
from django.utils.timezone import now

User = get_user_model()  # Recommended way to get User model

class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    doctor_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    degree = models.CharField(max_length=200, blank=True)
    age = models.IntegerField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True,null=True)  # Removed null=True
    gender = models.CharField(max_length=9, blank=True)

    def __str__(self):
        return self.username

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    patient_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True, null=True)
    age = models.IntegerField(null=True, blank=True)
    address = models.TextField(blank=True,null=True)
    mobile_number = models.CharField(max_length=15, blank=True,null=True)  # Removed null=True
    gender = models.CharField(max_length=9, blank=True)

    def __str__(self):
        return self.username

class Prescription(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,null=True)
    date = models.DateField(default=date.today, null=True)  # Used default instead of auto_now_add
    details = models.TextField(blank=True,null=True)

    def __str__(self):
        return "Prescription for {self.patient.username} on {self.date}"

class Receptionist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    receptionist_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.username

# Function to create a default receptionist user after migrations
from django.db.models.signals import post_migrate
from django.apps import apps

def create_default_receptionist(sender, **kwargs):
    if sender.name == 'patient_history':  # Ensure it runs only for this app
        default_username = "receptionist"
        default_password = "12345"

        if not User.objects.filter(username=default_username).exists():
            user = User.objects.create_user(username=default_username, password=default_password)
            Receptionist.objects.create(user=user, username=default_username)
            print("Default receptionist account created.")

post_migrate.connect(create_default_receptionist, sender=apps.get_app_config('patient_history'))

class Appointment(models.Model):
    appointment_date = models.DateField()
    appointment_time = models.TimeField(default=now)  # Added time field
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    def __str__(self):
        return f"Appointment on {self.appointment_date} at {self.appointment_time} with Dr. {self.doctor.username}"
