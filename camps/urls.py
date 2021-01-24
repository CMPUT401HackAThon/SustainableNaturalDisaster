from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Inventory/', views.InventoryListView.as_view(),
         name='Inventory-list'),
    path('Inventory/create', views.InventoryCreateView.as_view(),
         name='Inventory-create'),
    path('Inventory/create_request', views.InventoryCreateRequestView.as_view(),
         name='Inventory-create_request'),
    path('Inventory/<int:pk>/delete', views.InventoryDeleteView.as_view(),
         name='Inventory-delete'),     
    path('Inventory/<int:pk>', views.InventoryDetailView.as_view(),
         name='Inventory-detail'),
    path('Inventory/<int:pk>/update', views.InventoryUpdateView.as_view(),
         name='Inventory-update'),
    
    path('supply_requests/', views.supplyRequests, name='supply_requests'),
    path('fullfill_request/<request_id>', views.fullfill_request, name='fullfill_req'),
    # path('camp_inventory/', views.camp_inv, name='camp_inv')
]