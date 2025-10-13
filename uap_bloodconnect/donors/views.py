from django.shortcuts import render, get_object_or_404, redirect
from .models import Donor
from .forms import DonorForm

#READ - Show list of donors
def donor_list(request):
    donors = Donor.objects.all()
    return render(request, 'donors/donor_list.html', {'donors': donors})

#CREATE - Add new donor
def donor_create(request):
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm()
    return render(request, 'donors/donor_form.html', {'form': form})

#UPDATE - Edit donor info
def donor_update(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, request.FILES, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm(instance=donor)
    return render(request, 'donors/donor_form.html', {'form': form})

#DELETE - Remove donor
def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        return redirect('donor_list')
    return render(request, 'donors/donor_confirm_delete.html', {'donor': donor})