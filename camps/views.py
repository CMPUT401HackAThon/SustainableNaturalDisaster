from django.shortcuts import render, redirect
from .models import SupplyReqs, Inventory
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

def home(request):
    sc = SupplyReqs.objects.filter(fullfilled = False)
    total_reqs = sc.count()
    return render(request, 'home.html', {"total_reqs":total_reqs})

# def camp_inv(request):
#     return render(request, 'camp_inv.html', {})

def supplyRequests(request):
    current_user = request.user
    all_camp_reqs = SupplyReqs.objects.all
    return render(request, 'supplyRequests.html', {'all_camp_reqs': all_camp_reqs, 'all_inventories': Inventory, 'current_user': current_user})


class InventoryListView(ListView):

    model = Inventory
    template_name = 'Inventory/list.html'
    context_object_name = 'Inventorys'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(InventoryListView, self).get_context_data(**kwargs)
        Inventorys = self.get_queryset()
        page = self.request.GET.get('page')
        paginator = Paginator(Inventorys, self.paginate_by)
        try:
            Inventorys = paginator.page(page)
        except PageNotAnInteger:
            Inventorys = paginator.page(1)
        except EmptyPage:
            Inventorys = paginator.page(paginator.num_pages)
        context['Inventorys'] = Inventorys
        return context


class InventoryCreateView(CreateView):
    model = Inventory
    template_name = 'Inventory/create.html'
    fields = ('camp_id','item_id', 'item_amt', )
    success_url = reverse_lazy('Inventory-list')


class InventoryDetailView(DetailView):

    model = Inventory
    template_name = 'Inventory/detail.html'
    context_object_name = 'Inventory'


class InventoryUpdateView(UpdateView):

    model = Inventory
    template_name = 'Inventory/update.html'
    context_object_name = 'Inventory'
    fields = ('item_id', 'item_amt',)

    def get_success_url(self):
        return reverse_lazy('Inventory-detail', kwargs={'pk': self.object.id})


class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = 'Inventory/delete.html'
    context_object_name = 'Inventory'
    success_url = reverse_lazy('Inventory-list')


    
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
