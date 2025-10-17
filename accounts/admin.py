from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'uap_id', 'user_type', 'email', 'is_verified', 'date_joined')
    list_filter = ('user_type', 'is_verified', 'date_joined')
    fieldsets = UserAdmin.fieldsets + (
        ('UAP Information', {'fields': ('uap_id', 'user_type', 'phone_number', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('UAP Information', {'fields': ('uap_id', 'user_type', 'phone_number', 'email')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'total_donations', 'points')
    list_filter = ('blood_group',)
    search_fields = ('user__username', 'user__uap_id')