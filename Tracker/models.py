from django.db import models
from datetime import datetime
# Create your models here.


class MstDepartment(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    floor_number = models.PositiveIntegerField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class MstTrackerStatus(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class TrackerMaster(models.Model):
    from_department = models.ForeignKey(MstDepartment, on_delete=models.DO_NOTHING)
    to_department = models.ForeignKey(MstDepartment, on_delete=models.DO_NOTHING)
    reason = models.TextField(null=False, blank=False)
    reported_date = models.DateTimeField(null=False, blank=False, default=datetime.now())
    complaint_status = models.ForeignKey(MstTrackerStatus, on_delete=models.DO_NOTHING)
