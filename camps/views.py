from django.shortcuts import render
from .models import SupplyReqs, Inventory

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
    return render(request, 'home.html', {})

def supplyRequests(request):
    current_user = request.user
    all_camp_reqs = SupplyReqs.objects.all
    return render(request, 'supplyRequests.html', {'all_camp_reqs': all_camp_reqs, 'all_inventories': Inventory, 'current_user': current_user})

@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class InventoryCreateView(CreateView):
    model = Inventory
    template_name = 'Inventory/create.html'
    fields = ('item_id', 'item_amt', )
    success_url = reverse_lazy('Inventory-list')


@method_decorator(login_required, name='dispatch')
class InventoryDetailView(DetailView):

    model = Inventory
    template_name = 'Inventory/detail.html'
    context_object_name = 'Inventorys'


@method_decorator(login_required, name='dispatch')
class InventoryUpdateView(UpdateView):

    model = Inventory
    template_name = 'Inventory/update.html'
    context_object_name = 'Inventorys'
    fields = ('item_id', 'item_amt',)

    def get_success_url(self):
        return reverse_lazy('Inventory-detail', kwargs={'pk': self.object.id})


@method_decorator(login_required, name='dispatch')
class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = 'Inventory/delete.html'
    success_url = reverse_lazy('Inventory-list')
