from django.db import models

class SupplyReqs(models.Model):
    camp_id = models.CharField(max_length=30)
    fullfilled = models.BooleanField(default=False)
    item_id = models.CharField(max_length=30)
    item_amt = models.PositiveIntegerField()

    def __str__(self):
        return self.camp_id + ' | ' + self.item_id + ' | ' + str(self.item_amt) + ' | ' + str(self.fullfilled)


