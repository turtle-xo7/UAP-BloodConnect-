from django.shortcuts import render, get_object_or_404, redirect
from .models import BloodRequest, Hospital
from .forms import BloodRequestForm

def request_list(request):
    qs = BloodRequest.objects.filter(fulfilled=False)
    bg = request.GET.get('bg')
    urgency = request.GET.get('urgency')
    if bg:
        qs = qs.filter(blood_groupiexact=bg)
    if urgency:
        qs = qs.filter(urgencyiexact=urgency)
    return render(request, 'bloodrequests/request_list.html', {'requests': qs})

def request_detail(request, pk):
    req = get_object_or_404(BloodRequest, pk=pk)
    return render(request, 'bloodrequests/request_detail.html', {'request_obj': req})

def request_create(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('request_list')
    else:
        form = BloodRequestForm()
    return render(request, 'bloodrequests/request_form.html', {'form': form})

def request_update(request, pk):
    req = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        form = BloodRequestForm(request.POST, request.FILES, instance=req)
        if form.is_valid():
            form.save()
            return redirect('request_detail', pk=req.pk)
    else:
        form = BloodRequestForm(instance=req)
    return render(request, 'bloodrequests/request_form.html', {'form': form})

def request_delete(request, pk):
    req = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        req.delete()
        return redirect('request_list')
    return render(request, 'bloodrequests/request_confirm_delete.html', {'request_obj': req})