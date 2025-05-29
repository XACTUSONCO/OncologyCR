from django.contrib import admin
from .models import Patient, Leave
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.register(Patient)

class LeaveResource(resources.ModelResource):
    class Meta:
        model = Leave

class LeaveAdmin(ImportExportModelAdmin):
    resource_class = LeaveResource
    list_filter = ['is_deleted']
    list_display = ['is_deleted', 'name', 'from_date', 'kind']
    ordering = ['-from_date']

admin.site.register(Leave, LeaveAdmin)
