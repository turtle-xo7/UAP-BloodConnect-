from django.db import models
from accounts.models import CustomUser


class BloodGroup(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES, unique=True)

    def __str__(self):
        return self.blood_type

    def get_compatible_groups(self):
        compatibility = {
            'A+': ['A+', 'AB+'],
            'A-': ['A+', 'A-', 'AB+', 'AB-'],
            'B+': ['B+', 'AB+'],
            'B-': ['B+', 'B-', 'AB+', 'AB-'],
            'O+': ['A+', 'B+', 'O+', 'AB+'],
            'O-': ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'],
            'AB+': ['AB+'],
            'AB-': ['AB+', 'AB-'],
        }
        return compatibility.get(self.blood_type, [])


class Donor(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('unavailable', 'Unavailable'),
    ]

    LOCATION_CHOICES = [
        ('campus', 'UAP Campus'),
        ('uttara', 'Uttara'),
        ('gulshan', 'Gulshan'),
        ('banani', 'Banani'),
        ('dhanmondi', 'Dhanmondi'),
        ('mirpur', 'Mirpur'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)
    availability_status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='available')
    can_donate_again = models.BooleanField(default=True)
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES, default='campus')
    emergency_response = models.BooleanField(default=False)
    last_donation_date = models.DateField(null=True, blank=True)
    total_donations = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"

    def update_availability(self):
        from datetime import date, timedelta
        if self.last_donation_date:
            days_since_last_donation = (date.today() - self.last_donation_date).days
            self.can_donate_again = days_since_last_donation >= 90
            self.save()


class DonationHistory(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='donations')
    donation_date = models.DateField()
    units_donated = models.DecimalField(max_digits=3, decimal_places=1, default=1.0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='completed')
    hospital = models.CharField(max_length=200, blank=True)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.user.username} - {self.donation_date}"


class Achievement(models.Model):
    BADGE_TYPES = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
        ('hero', 'Hero'),
    ]

    donor = models.ForeignKey(Donor, on_delete=models.CASCADE, related_name='achievements')
    badge_type = models.CharField(max_length=10, choices=BADGE_TYPES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    achieved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor.user.username} - {self.badge_type} - {self.title}"