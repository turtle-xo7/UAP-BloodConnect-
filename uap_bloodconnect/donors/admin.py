from django.contrib import admin
from django.utils.html import format_html
from .models import Donor

class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'blood_group', 'is_available', 'profile_preview')
    readonly_fields = ('profile_preview',)
    fields = ('name', 'email', 'department', 'phone', 'blood_group', 'last_donation_date', 'is_available', 'profile_pic', 'profile_preview')

    def profile_preview(self, obj):
        if obj.profile_pic:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:50%;" />', obj.profile_pic.url)
        return "No profile picture"
    profile_preview.short_description = 'Profile Preview'

admin.site.register(Donor, DonorAdmin)