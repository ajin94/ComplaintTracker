from django.contrib import admin
from .models import *


class AdminDepartment(admin.ModelAdmin):
    list_display = ['name', 'floor_number', 'contact_number', 'created_date', 'updated_date']


class AdminTrackMaster(admin.ModelAdmin):
    list_display = ('complaint_id', 'from_department', 'to_department', 'reason', 'reported_date',
                    'priority', 'complaint_status')


class AdminPriority(admin.ModelAdmin):
    list_display = ('name', 'created_date', 'updated_date')


class AdminTrackerStatus(admin.ModelAdmin):
    list_display = ('name', 'created_date', 'updated_date')

admin.site.register(TrackerMaster, AdminTrackMaster)
admin.site.register(Department, AdminDepartment)
admin.site.register(Priority, AdminPriority)
admin.site.register(TrackerStatus, AdminTrackerStatus)

admin.site.site_header = "STARCARE- Tracker"
admin.site.site_title = "Complaint Tracker"
