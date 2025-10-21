from django.db import models
from accounts.models import CustomUser
import os




def donation_certificate_path(instance, filename):
   # file will be uploaded to MEDIA_ROOT/certificates/donor_<id>/<filename>
   ext = filename.split('.')[-1]
   filename = f'certificate_{instance.donor.id}_{instance.id}.{ext}'
   return os.path.join('certificates', f'donor_{instance.donor.id}', filename)




def achievement_badge_path(instance, filename):
   # file will be uploaded to MEDIA_ROOT/badges/achievement_<id>/<filename>
   ext = filename.split('.')[-1]
   filename = f'badge_{instance.id}.{ext}'
   return os.path.join('badges', f'achievement_{instance.id}', filename)




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
   certificate = models.FileField(
       upload_to=donation_certificate_path,
       blank=True,
       null=True,
       help_text="Upload donation certificate (PDF, JPG, PNG)"
   )
   created_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return f"{self.donor.user.username} - {self.donation_date}"


   def delete(self, *args, **kwargs):
       # Delete certificate file when donation record is deleted
       if self.certificate:
           if os.path.isfile(self.certificate.path):
               os.remove(self.certificate.path)
       super().delete(*args, **kwargs)




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
   badge_icon = models.ImageField(
       upload_to=achievement_badge_path,
       blank=True,
       null=True,
       help_text="Badge icon image"
   )
   achieved_at = models.DateTimeField(auto_now_add=True)


   def __str__(self):
       return f"{self.donor.user.username} - {self.badge_type} - {self.title}"


   def delete(self, *args, **kwargs):
       # Delete badge icon when achievement is deleted
       if self.badge_icon:
           if os.path.isfile(self.badge_icon.path):
               os.remove(self.badge_icon.path)
       super().delete(*args, **kwargs)


