from django.db import models
from datetime import datetime
# Create your models here.


class Department(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    floor_number = models.PositiveIntegerField(null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}, floor no. {}'.format(self.name, self.floor_number)


class TrackerStatus(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s' % self.name


class TrackerMaster(models.Model):
    department_reporting = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    department_reported = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    reason = models.TextField(null=False, blank=False)
    reported_date = models.DateTimeField(null=False, blank=False, default=datetime.now())
    complaint_status = models.ForeignKey(TrackerStatus, on_delete=models.DO_NOTHING)
    updated_date = models.DateTimeField(auto_now=True)
