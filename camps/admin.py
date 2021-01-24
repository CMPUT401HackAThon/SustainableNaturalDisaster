from django.contrib import admin
from .models import SupplyReqs
from .models import Inventory
#from .models import test_2


admin.site.register(Inventory)
admin.site.register(SupplyReqs)

