from django import forms
from django.contrib.auth.models import User
from .models import Patient,Doctor,Prescription

class SignupForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),

    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class PatientForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    age = forms.IntegerField(min_value=0)
    address = forms.CharField(widget=forms.Textarea)
    mobile_number = forms.CharField(max_length=15)

    class Meta:
        model = Patient
        fields = ['age', 'gender', 'address', 'mobile_number']

class DoctorForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    ]

    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect)
    mobile_number = forms.CharField(max_length=15)  # Change 'mobile' to 'mobile_number'
    experience = forms.IntegerField(min_value=0)
    degree = forms.CharField(max_length=200)

    class Meta:
        model = Doctor
        fields = ['age', 'mobile_number', 'gender', 'experience', 'degree']  # Use 'mobile_number'


class PrescriptionForm(forms.ModelForm):
    patient_id = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Patient ID'})
    )

    class Meta:
        model = Prescription
        fields = ['date', 'details']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'details': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
