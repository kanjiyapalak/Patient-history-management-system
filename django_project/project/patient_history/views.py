from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import SignupForm
from .models import Doctor, Patient, Receptionist,Appointment,Prescription
from .forms import PatientForm,DoctorForm,PrescriptionForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Doctor, Patient, Appointment
from django.utils.timezone import now


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        # Check if username and password are for the default receptionist
        if role == "receptionist" and username == "receptionist" and password == "12345":
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('receptionist_dashboard')

        # Authenticate normal users
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if role == "doctor" and Doctor.objects.filter(user=user).exists():
                return redirect('doctor_dashboard')
            elif role == "patient" and Patient.objects.filter(user=user).exists():
                return redirect('patient_dashboard')
            elif role == "receptionist" and Receptionist.objects.filter(user=user).exists():
                return redirect('receptionist_dashboard')
            else:
                messages.error(request, "Invalid role selected.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash password
            user.save()

            role = form.cleaned_data['role']

            if role == "doctor":
                request.session['user_id'] = user.id  # Store user ID temporarily
                return redirect('add_doctor_details')
            elif role == "patient":
                request.session['patient_user_id'] = user.id  # Store user ID in session
                return redirect('add_patient_details')  # Redirect to patient details form

            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def receptionist_dashboard(request):
    return render(request, 'receptionist_dashboard.html')

@login_required
def doctor_dashboard(request):
    """Fetch and display the logged-in doctor's details dynamically."""
    doctor = None  # Default value in case doctor does not exist
    
    if hasattr(request.user, 'doctor'):  # Check if user has an associated doctor profile
        doctor = request.user.doctor  

    if not doctor:  # If doctor record doesn't exist, redirect to login
        return redirect('login')

    return render(request, 'doctor_dashboard.html', {'doctor': doctor})

@login_required
def patient_dashboard(request):
    """Fetch and display the logged-in patient's details dynamically."""
    patient = None  # Default value in case patient does not exist

    if hasattr(request.user, 'patient'):  # Check if user has an associated patient profile
        patient = request.user.patient  

    if not patient:  # If patient record doesn't exist, redirect to login
        return redirect('login')

    return render(request, 'patient_dashboard.html', {'patient': patient})

def add_patient_details(request):
    if 'patient_user_id' not in request.session:
        return redirect('signup')  # Redirect if session is lost

    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            user = User.objects.get(id=request.session['patient_user_id'])
            patient = form.save(commit=False)
            patient.user = user
            patient.username = user.username
            patient.email = user.email
            patient.save()

            del request.session['patient_user_id']  # Remove session data
            messages.success(request, "Patient details added successfully! Please log in.")
            return redirect('login')

    else:
        form = PatientForm()

    return render(request, 'add_patient_details.html', {'form': form})


def add_doctor_details(request):
    user_id = request.session.get('user_id')  # Get user ID from session

    if not user_id:
        return redirect('signup')  # Redirect if no user ID is found

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        form = DoctorForm(request.POST)
        if form.is_valid():
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.username = user.username
            doctor.email = user.email
            doctor.save()

            del request.session['user_id']  # Remove user ID from session
            messages.success(request, "Doctor details added successfully! Please log in.")
            return redirect('login')
    else:
        form = DoctorForm()

    return render(request, 'add_doctor_details.html', {'form': form})

@login_required
def update_profile(request):
    """Handles profile updates for the logged-in doctor."""
    doctor = request.user.doctor  # Fetch the logged-in doctor's record

    if request.method == "POST":
        doctor.email = request.POST.get("email")
        doctor.age = request.POST.get("age")
        doctor.mobile_number = request.POST.get("mobile_number")
        doctor.degree = request.POST.get("degree")
        doctor.experience = request.POST.get("experience")
        doctor.save()
        return redirect('doctor_dashboard')

    return render(request, 'update_profile.html', {'doctor': doctor})

@login_required
def delete_profile(request):
    """Deletes the doctor's profile and logs them out."""
    doctor = request.user.doctor
    doctor.delete()
    return redirect('login')

def view_details(request):
    # Assuming you want to fetch the logged-in doctor's details
     doctor = get_object_or_404(Doctor, username=request.user.username)
     return render(request, 'view_details.html', {'doctor': doctor})

def manage_profile(request):
    doctor = get_object_or_404(Doctor, username=request.user.username)
    return render(request, 'manage_profile.html', {'doctor': doctor})

@login_required
def update_patient_profile(request):
    """Handles profile updates for the logged-in patient."""
    patient = request.user.patient  # Fetch the logged-in patient's record

    if request.method == "POST":
        patient.email = request.POST.get("email")
        patient.age = request.POST.get("age")
        patient.mobile_number = request.POST.get("mobile_number")
        patient.address = request.POST.get("address")
        patient.description = request.POST.get("description")
        patient.save()
        return redirect('patient_dashboard')

    return render(request, 'patient_dashboard.html', {'patient': patient})

@login_required
def delete_patient_profile(request):
    """Deletes the patient's profile and logs them out."""
    patient = request.user.patient
    patient.delete()
    return redirect('login')

@login_required  
def manage_prescription(request):
    return render(request, 'manage_prescription.html')

@login_required
def add_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)

            # Get patient instance
            patient_id = request.POST.get("patient_id")  # Get patient ID from form
            patient = get_object_or_404(Patient, pk=patient_id)  # Fetch Patient object

            prescription.patient = patient  # Assign the Patient object (not ID)
            prescription.save()

            return render(request, "add_prescription.html", {"message": "Prescription added successfully!"})
    else:
        form = PrescriptionForm()

    return render(request, "add_prescription.html", {"form": form})

@login_required
def view_prescription(request):
    prescriptions = []  # Default empty list
    patient_id = request.GET.get("patient_id")  # Get the patient ID from request

    if patient_id and patient_id.isdigit():  # Ensure valid ID
        patient_id = int(patient_id)  # Convert to integer
        try:
            prescriptions = Prescription.objects.filter(patient_id=patient_id)
        except Exception as e:
            print(f"Error fetching prescriptions: {e}")  # Debugging
            prescriptions = []

    return render(request, "view_prescription.html", {
        "prescriptions": prescriptions,
        "patient_id": patient_id
    })

@login_required
def doctor_show_appointments(request):
    # Get the doctor instance associated with the logged-in user
    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        doctor = None

    if doctor:
        appointments = Appointment.objects.filter(doctor=doctor)
    else:
        appointments = []

    return render(request, "doctor_show_appointments.html", {"appointments": appointments})


@login_required
def patient_view_prescription(request):
    try:
        patient = Patient.objects.get(user=request.user)
        prescriptions = Prescription.objects.filter(patient=patient)
    except Patient.DoesNotExist:
        prescriptions = None

    return render(request, 'prescription_partial.html', {'prescriptions': prescriptions})

@login_required
def patient_show_appointment(request):
    try:
        # Get the logged-in patient instance
        patient = Patient.objects.get(user=request.user)  # Ensure 'user' is linked to Patient

        # Fetch appointments related to the logged-in patient
        appointments = Appointment.objects.filter(patient=patient)

        return render(request, 'partial_appointment.html', {'appointments': appointments})

    except Patient.DoesNotExist:
        return render(request, 'partial_appointment.html', {'error': "Patient profile not found."})

@login_required
def add_appointment(request):
    if request.method == "POST":
        print("Form Submission Started!")
        print(request.POST)  # Debugging

        doctor_id = request.POST.get("doctor_id")
        patient_id = request.POST.get("patient_id")
        appointment_date = request.POST.get("appointment_date")
        appointment_time = request.POST.get("appointment_time")

        print(f"Received Data - Doctor ID: {doctor_id}, Patient ID: {patient_id}, Date: {appointment_date}, Time: {appointment_time}")

        try:
            doctor = Doctor.objects.get(doctor_id=int(doctor_id))
            patient = Patient.objects.get(patient_id=int(patient_id))
            print(f"Doctor: {doctor}, Patient: {patient}")
        except Doctor.DoesNotExist:
            messages.error(request, "Doctor not found!")
            print("Doctor not found!")
            return render(request, "add_appointment.html")  # Stay on the same page
        except Patient.DoesNotExist:
            messages.error(request, "Patient not found!")
            print("Patient not found!")
            return render(request, "add_appointment.html")  # Stay on the same page

        try:
            # Save appointment
            appointment = Appointment(
                doctor=doctor,
                patient=patient,
                appointment_date=appointment_date,
                appointment_time=appointment_time or now().time()
            )
            appointment.save()
            print("Appointment successfully saved!")
        except Exception as e:
            print(f"Error saving appointment: {e}")
            messages.error(request, "Failed to save appointment!")
            return render(request, "add_appointment.html")  # Stay on the same page

    return render(request, "add_appointment.html")  # Default GET request


    # Stay on the same page and reload doctors and patients
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()
    return render(request, "add_appointment.html", {"doctors": doctors, "patients": patients})


def manage_appointments(request):
    appointments = Appointment.objects.all()
    return render(request, "manage_appointments.html", {"appointments": appointments})

def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    doctors = Doctor.objects.all()
    patients = Patient.objects.all()

    if request.method == "POST":
        appointment.doctor_id = request.POST["doctor_id"]
        appointment.patient_id = request.POST["patient_id"]
        appointment.appointment_date = request.POST["appointment_date"]
        appointment.appointment_time = request.POST["appointment_time"]
        appointment.save()
        return redirect("manage_appointments")

    return render(request, "update_appointment.html", {
        "appointment": appointment,
        "doctors": doctors,
        "patients": patients
    })


def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment.delete()
    messages.success(request, "Appointment deleted successfully!")
    return redirect("manage_appointments")

def show_appointments(request):
    patient = None
    appointments = []
    
    if 'patient_id' in request.GET:
        patient_id = request.GET.get('patient_id')
        try:
            patient = Patient.objects.get(patient_id=patient_id)  # <-- Change here
            appointments = Appointment.objects.filter(patient=patient)
        except Patient.DoesNotExist:
            patient = None

    return render(request, 'show_appointments.html', {'patient': patient, 'appointments': appointments})







