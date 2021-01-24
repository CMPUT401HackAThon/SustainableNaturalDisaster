from django.shortcuts import render, redirect
from .models import SupplyReqs, Inventory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html', {})

def camp_inv(request):
    return render(request, 'camp_inv.html', {})

def supplyRequests(request):
    current_user = request.user
    all_camp_reqs = SupplyReqs.objects.all
    return render(request, 'supplyRequests.html', {'all_camp_reqs': all_camp_reqs, 'all_inventories': Inventory, 'current_user': current_user})

def fullfill_request(request, request_id):
    supply_req = SupplyReqs.objects.get(pk=request_id)
    req_amt = supply_req.item_amt

    # Check if user has items for request
    sc = Inventory.objects.filter(item_id=supply_req.item_id, camp_id=request.user.username)
    if sc.count() > 0:
        camp_inventory = Inventory.objects.get(item_id=supply_req.item_id, camp_id=request.user.username)

        # Check if user if fullfilling own request
        if supply_req.camp_id == request.user.username:
            messages.success(request, ("You can't fullfill your own request"))
        elif camp_inventory.item_amt > req_amt:
            
            # Check if requester has item in their database
            sc = Inventory.objects.filter(item_id=supply_req.item_id, camp_id=supply_req.camp_id)
            if sc.count() > 0:
                req_inventory = Inventory.objects.get(item_id=supply_req.item_id, camp_id=supply_req.camp_id)
                req_inventory.item_amt = req_inventory.item_amt + req_amt
            else:
                req_inventory = Inventory(camp_id=supply_req.camp_id, item_id=supply_req.item_id, item_amt=supply_req.item_amt)
            
            # Finish with supply request transaction
            camp_inventory.item_amt = camp_inventory.item_amt - req_amt
            supply_req.fullfilled = True
            supply_req.save()
            req_inventory.save()
            camp_inventory.save()
            messages.success(request, ("The supply request has been fullfilled"))
        else:
            messages.success(request, ("Your camp lacks the supplies to fullfill this request"))
    else:
        messages.success(request, ("Your camp does not carry these supplies"))

    return redirect('supply_requests')
