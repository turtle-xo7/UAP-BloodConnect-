from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime
from .models import BloodRequest, RequestResponse, Notification
from .forms import BloodRequestForm, RequestResponseForm
from donors.models import Donor, BloodGroup


@login_required
def create_request(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST, request.FILES)
        if form.is_valid():
            blood_request = form.save(commit=False)
            blood_request.requester = request.user
            blood_request.save()

            messages.success(request, 'Blood request created successfully! Donors will be notified.')
            return redirect('request_detail', request_id=blood_request.id)
    else:
        form = BloodRequestForm()

    return render(request, 'requests/create_request.html', {'form': form})


@login_required
def request_list(request):
    requests = BloodRequest.objects.all().select_related('requester', 'blood_group').order_by('-created_at')

    blood_group_filter = request.GET.get('blood_group')
    status_filter = request.GET.get('status')
    urgency_filter = request.GET.get('urgency')
    location_filter = request.GET.get('location')

    if blood_group_filter:
        requests = requests.filter(blood_group__blood_type=blood_group_filter)
    if status_filter:
        requests = requests.filter(status=status_filter)
    if urgency_filter:
        requests = requests.filter(urgency=urgency_filter)
    if location_filter:
        requests = requests.filter(location=location_filter)

    context = {
        'requests': requests,
        'blood_groups': BloodGroup.objects.all(),
    }
    return render(request, 'requests/request_list.html', context)


@login_required
def request_detail(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    user_response = None
    if hasattr(request.user, 'donor'):
        user_response = RequestResponse.objects.filter(
            blood_request=blood_request,
            donor=request.user.donor
        ).first()

    responses = RequestResponse.objects.filter(blood_request=blood_request).select_related('donor__user',
                                                                                           'donor__blood_group')

    if request.method == 'POST' and hasattr(request.user, 'donor'):
        form = RequestResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.blood_request = blood_request
            response.donor = request.user.donor
            response.save()
            messages.success(request, 'Your response has been submitted!')
            return redirect('request_detail', request_id=request_id)
    else:
        form = RequestResponseForm()

    context = {
        'blood_request': blood_request,
        'responses': responses,
        'user_response': user_response,
        'form': form,
        'can_respond': hasattr(request.user, 'donor') and not user_response,
    }
    return render(request, 'requests/request_detail.html', context)


@login_required
def my_requests(request):
    my_requests = BloodRequest.objects.filter(requester=request.user).order_by('-created_at')
    return render(request, 'requests/my_requests.html', {'my_requests': my_requests})


@login_required
def respond_to_request(request, request_id):
    blood_request = get_object_or_404(BloodRequest, id=request_id)

    if not hasattr(request.user, 'donor'):
        messages.error(request, 'You need to be registered as a donor to respond to requests.')
        return redirect('donor_register')

    if RequestResponse.objects.filter(blood_request=blood_request, donor=request.user.donor).exists():
        messages.info(request, 'You have already responded to this request.')
        return redirect('request_detail', request_id=request_id)

    if request.method == 'POST':
        form = RequestResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.blood_request = blood_request
            response.donor = request.user.donor
            response.save()
            messages.success(request, 'Thank you for responding to this blood request!')
            return redirect('request_detail', request_id=request_id)
    else:
        form = RequestResponseForm()

    return render(request, 'requests/respond.html', {'form': form, 'blood_request': blood_request})