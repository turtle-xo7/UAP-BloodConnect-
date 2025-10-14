from django import forms
from .models import BloodRequest

class BloodRequestForm(forms.ModelForm):
    date_needed = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    class Meta:
        model = BloodRequest
        fields = ['requester_name','requester_contact','blood_group','units_required','date_needed',
                  'location','related_donor','hospital','urgency','note','proof_image']