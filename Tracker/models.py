from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Priority(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.name)


class Department(models.Model):
    name = models.CharField(max_length=150, null=False, blank=False)
    floor_number = models.PositiveIntegerField(null=False, blank=False)
    contact_number = models.CharField(max_length=14, null=True, blank=True)
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

    class Meta:
        verbose_name_plural = 'Tracker Status'


class TrackerUsers(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.DO_NOTHING)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Users'


def generate_tracker_id():
    return "CTID#{}".format(TrackerMaster.objects.count()+1)


class TrackerMaster(models.Model):
    complaint_id = models.CharField(max_length=50, null=False, blank=False, default=generate_tracker_id)
    from_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name='from_department')
    to_department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, related_name='to_department')
    reason = models.TextField(null=False, blank=False)
    reported_date = models.DateTimeField(null=False, blank=False, default=datetime.now())
    priority = models.ForeignKey(Priority, null=True, blank=True, on_delete=models.DO_NOTHING)
    complaint_status = models.ForeignKey(TrackerStatus, on_delete=models.DO_NOTHING, default=1)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Complaint Tracker'


def create_tracker_users(sender, **kwargs):
    if kwargs['created']:
        TrackerUsers.objects.create(user=kwargs['instance'])


post_save.connect(create_tracker_users, sender=User)
