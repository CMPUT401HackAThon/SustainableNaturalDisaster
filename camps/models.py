from django.db import models

# Create your models here.
class Camp(models.Model):
    camp_name = models.CharField(max_length=50,primary_key=True)
    water = models.IntegerField(max_length=1,help_text="Water storage capacity",editable=True)
    food = models.IntegerField(max_length=1,help_text="Food storage capacity",editable=True)
    blanket = models.IntegerField(max_length=1,help_text="Blanket storage capacity",editable=True)
    drug = models.IntegerField(max_length=1,help_text="Drug storage capacity",editable=True)