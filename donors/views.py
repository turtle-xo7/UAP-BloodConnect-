from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Donor, DonationHistory, Achievement, BloodGroup
from .forms import DonorRegistrationForm, DonationHistoryForm


@login_required
def donor_dashboard(request):
    try:
        donor = Donor.objects.get(user=request.user)
        donation_history = DonationHistory.objects.filter(donor=donor).order_by('-donation_date')[:5]
        achievements = Achievement.objects.filter(donor=donor)

        context = {
            'donor': donor,
            'donation_history': donation_history,
            'achievements': achievements,
        }
        return render(request, 'donors/dashboard.html', context)
    except Donor.DoesNotExist:
        return redirect('donor_register')


@login_required
def donor_register(request):
    if hasattr(request.user, 'donor'):
        messages.info(request, 'You are already registered as a donor.')
        return redirect('donor_dashboard')

    if request.method == 'POST':
        form = DonorRegistrationForm(request.POST)
        if form.is_valid():
            donor = form.save(commit=False)
            donor.user = request.user
            donor.save()
            messages.success(request, 'Successfully registered as a donor! Thank you for saving lives.')
            return redirect('donor_dashboard')
    else:
        form = DonorRegistrationForm()

    return render(request, 'donors/register.html', {'form': form})


@login_required
def donor_directory(request):
    donors = Donor.objects.filter(availability_status='available').select_related('user', 'blood_group')
    blood_groups = BloodGroup.objects.all()

    blood_group_filter = request.GET.get('blood_group')
    location_filter = request.GET.get('location')

    if blood_group_filter:
        donors = donors.filter(blood_group__blood_type=blood_group_filter)
    if location_filter:
        donors = donors.filter(location=location_filter)

    context = {
        'donors': donors,
        'blood_groups': blood_groups,
        'selected_blood_group': blood_group_filter,
        'selected_location': location_filter,
    }
    return render(request, 'donors/directory.html', context)


@login_required
def add_donation_history(request):
    try:
        donor = Donor.objects.get(user=request.user)
    except Donor.DoesNotExist:
        messages.error(request, 'You need to register as a donor first.')
        return redirect('donor_register')

    if request.method == 'POST':
        form = DonationHistoryForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = donor
            donation.status = 'completed'
            donation.save()

            donor.total_donations += 1
            donor.last_donation_date = donation.donation_date
            donor.save()

            messages.success(request, 'Donation history added successfully!')
            return redirect('donor_dashboard')
    else:
        form = DonationHistoryForm()

    return render(request, 'donors/add_donation.html', {'form': form})


@login_required
def donation_history(request):
    try:
        donor = Donor.objects.get(user=request.user)
        donations = DonationHistory.objects.filter(donor=donor).order_by('-donation_date')
        return render(request, 'donors/donation_history.html', {'donations': donations})
    except Donor.DoesNotExist:
        messages.error(request, 'You need to register as a donor first.')
        return redirect('donor_register')