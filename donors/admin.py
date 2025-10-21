from django.contrib import admin
from .models import BloodGroup, Donor, DonationHistory, Achievement


@admin.register(BloodGroup)
class BloodGroupAdmin(admin.ModelAdmin):
   list_display = ['blood_type']
   list_display_links = ['blood_type']


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
   list_display = ['user', 'blood_group', 'availability_status', 'location', 'emergency_response', 'total_donations']
   list_filter = ['blood_group', 'availability_status', 'location', 'emergency_response']
   search_fields = ['user__username', 'user__uap_id', 'user__email']
   readonly_fields = ['created_at']


@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
   list_display = ['donor', 'donation_date', 'units_donated', 'status', 'hospital']
   list_filter = ['status', 'donation_date']
   search_fields = ['donor__user__username', 'hospital']
   readonly_fields = ['created_at']


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
   list_display = ['donor', 'badge_type', 'title', 'achieved_at']
   list_filter = ['badge_type']
   search_fields = ['donor__user__username', 'title']
   readonly_fields = ['achieved_at']
