# models.py
from django.db import models
from django.contrib.auth.models import User

class FarmerData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    v1 = models.BooleanField()
    v2 = models.BooleanField()
    v3 = models.BooleanField()
    v4 = models.BooleanField()
    quantity = models.PositiveIntegerField()
    pinCode = models.CharField(max_length=10)
    time_slot = models.ForeignKey('TimeSlot', on_delete=models.SET_NULL, null=True)
    procurement_center = models.CharField(max_length=100, null=True)
    token = models.CharField(max_length=100, null=True)
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
