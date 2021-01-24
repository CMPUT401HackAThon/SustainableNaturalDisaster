from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('supply_requests/', views.supplyRequests, name='supply_requests'),
    path('fullfill_request/<request_id>', views.fullfill_request, name='fullfill_req'),
]