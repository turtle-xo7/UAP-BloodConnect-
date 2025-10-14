from django.contrib import admin
from django.utils.html import format_html
from .models import Hospital, BloodRequest

class HospitalAdmin(admin.ModelAdmin):
    list_display = ('name','contact')
    readonly_fields = ()

admin.site.register(Hospital, HospitalAdmin)

class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('requester_name','blood_group','units_required','date_needed','urgency','fulfilled','request_preview')
    readonly_fields = ('request_preview',)
    fields = ('requester_name','requester_contact','blood_group','units_required','date_needed','location','related_donor','hospital','urgency','note','proof_image','request_preview','fulfilled')

    def request_preview(self, obj):
        if obj.proof_image:
            return format_html('<img src="{}" width="140" style="object-fit:cover;"/>', obj.proof_image.url)
        return "No proof image"
    request_preview.short_description = 'Proof Preview'

admin.site.register(BloodRequest, BloodRequestAdmin)