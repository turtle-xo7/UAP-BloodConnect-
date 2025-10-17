from django import forms
from .models import BloodRequest, RequestResponse

class BloodRequestForm(forms.ModelForm):
    class Meta:
        model = BloodRequest
        fields = ['blood_group', 'urgency', 'location', 'needed_by_date', 'units_required', 'patient_name', 'patient_age', 'description', 'supporting_document']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'needed_by_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'units_required': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'min': '0.5', 'max': '10.0'}),
            'patient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter patient name'}),
            'patient_age': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '120'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Provide details about the patient and situation...'}),
        }
        labels = {
            'patient_name': 'Patient Full Name',
            'patient_age': 'Patient Age',
        }

class RequestResponseForm(forms.ModelForm):
    class Meta:
        model = RequestResponse
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a message for the requester (optional)...'}),
        }