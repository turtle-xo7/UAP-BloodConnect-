from django import forms
from .models import Donor, DonationHistory, BloodGroup


class DonorRegistrationForm(forms.ModelForm):
    blood_group = forms.ModelChoiceField(
        queryset=BloodGroup.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Blood Group"
    )

    class Meta:
        model = Donor
        fields = ['blood_group', 'location', 'emergency_response']
        widgets = {
            'location': forms.Select(attrs={'class': 'form-control'}),
            'emergency_response': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class DonationHistoryForm(forms.ModelForm):
    class Meta:
        model = DonationHistory
        fields = ['donation_date', 'units_donated', 'hospital', 'certificate']
        widgets = {
            'donation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'units_donated': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '0.5', 'min': '0.5', 'max': '2.0'}),
            'hospital': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hospital name'}),
        }