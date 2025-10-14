from django.db import models
from django.utils import timezone
from donors.models import Donor

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(blank=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    logo = models.ImageField(upload_to='hospital_logos/', blank=True, null=True)

    def str(self):
        return self.name

class BloodRequest(models.Model):
    URGENCY_CHOICES = [
        ('High', 'High'),
        ('Normal', 'Normal'),
    ]

    requester_name = models.CharField(max_length=200)
    requester_contact = models.CharField(max_length=50, blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUP_CHOICES)
    units_required = models.PositiveIntegerField(default=1)
    date_needed = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255, blank=True)
    related_donor = models.ForeignKey(Donor, on_delete=models.SET_NULL, blank=True, null=True, help_text="Optional: link to a donor")
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, blank=True, null=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='Normal')
    note = models.TextField(blank=True)
    proof_image = models.ImageField(upload_to='request_proofs/', blank=True, null=True)
    fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-urgency', 'date_needed', '-created_at']

    def str(self):
        return f"{self.blood_group} for {self.requester_name} ({self.urgency})"