from django.shortcuts import render
from django.db.models import Count
from donors.models import Donor, BloodGroup
from requests.models import BloodRequest


def home(request):
    total_donors = Donor.objects.count()
    active_requests = BloodRequest.objects.filter(status='open').count()
    blood_groups = BloodGroup.objects.all()

    context = {
        'total_donors': total_donors,
        'active_requests': active_requests,
        'blood_groups': blood_groups,
    }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')