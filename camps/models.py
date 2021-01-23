from django.db import models

# Create your models here.

class Inventory(models.Model):
    camp_id = models.CharField(max_length=30)
    item_id = models.CharField(max_length=30)
    item_amt = models.PositiveIntegerField()
