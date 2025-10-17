from django.contrib import admin
from .models import BloodRequest, RequestResponse, Notification

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'requester', 'blood_group', 'urgency', 'status', 'location', 'patient_name', 'created_at']
    list_filter = ['urgency', 'status', 'location', 'created_at']
    search_fields = ['requester__username', 'blood_group__blood_type', 'patient_name']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(RequestResponse)
class RequestResponseAdmin(admin.ModelAdmin):
    list_display = ['blood_request', 'donor', 'status', 'responded_at']
    list_filter = ['status', 'responded_at']
    search_fields = ['blood_request__id', 'donor__user__username']
    readonly_fields = ['responded_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title']
    readonly_fields = ['created_at']