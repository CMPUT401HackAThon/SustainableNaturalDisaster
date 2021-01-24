from django.shortcuts import render, redirect
from .models import SupplyReqs, Inventory
from django.contrib import messages

def home(request):
    return render(request, 'home.html', {})

def supplyRequests(request):
    current_user = request.user
    all_camp_reqs = SupplyReqs.objects.all
    return render(request, 'supplyRequests.html', {'all_camp_reqs': all_camp_reqs, 'all_inventories': Inventory, 'current_user': current_user})

def fullfill_request(request, request_id):
    supply_req = SupplyReqs.objects.get(pk=request_id)
    req_amt = supply_req.item_amt

    camp_inventory = Inventory.objects.get(item_id=supply_req.item_id, camp_id=request.user.username)
    if camp_inventory.item_amt > req_amt:
        camp_inventory.item_amt = camp_inventory.item_amt - req_amt
        req_inventory = Inventory.objects.get(item_id=supply_req.item_id, camp_id=supply_req.camp_id)
        req_inventory.item_amt = req_inventory.item_amt + req_amt
        supply_req.fullfilled = True
        supply_req.save()
        req_inventory.save()
        camp_inventory.save()
        messages.success(request, ("The supply request has been fullfilled"))
    else:
        messages.success(request, ("Your camp lacks the supplies to fullfill this request"))
    return redirect('supply_requests')
