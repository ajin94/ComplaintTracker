from django.db import models
from datetime import datetime
# Create your models here.


class MstDepartment(models.Model): pass


class UsersMaster(models.Model):
    user_name = mode


class MstTrackerStatus(models.Model): pass





class TrackerMaster(models.Model):
    from_department = models.ForeignKey(MstDepartment, on_delete=models.DO_NOTHING)
    to_department = models.ForeignKey(MstDepartment, on_delete=models.DO_NOTHING)
    reported_date = models.DateTimeField(null=False, blank=False, default=datetime.now())
    complaint_status = models.ForeignKey(MstTrackerStatus, on_delete=models.DO_NOTHING)
