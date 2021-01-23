from django.shortcuts import render
from .models import SupplyReqs

def home(request):
    return render(request, 'home.html', {})

def supplyRequests(request):
    current_user = request.user
    all_camp_reqs = SupplyReqs.objects.all
    return render(request, 'supplyRequests.html', {'all_camp_reqs': all_camp_reqs, 'current_user': current_user})
