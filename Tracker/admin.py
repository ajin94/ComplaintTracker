from django.contrib import admin
from .models import *


class AdminDepartment(admin.ModelAdmin):
    list_display = ['name', 'floor_number', 'contact_number', 'created_date', 'updated_date']


admin.site.register(Department, AdminDepartment)

admin.site.site_header = "STARCARE- Tracker"
admin.site.site_title = "Complaint Tracker"
