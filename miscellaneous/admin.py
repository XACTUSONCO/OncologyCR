from django.contrib import admin
from .models import CRO, Research_Management, Vendor, Supporting, Supporting_type, Delivery, QC

@admin.register(Supporting)
class SupportingAdmin(admin.ModelAdmin):
    list_filter = ['is_deleted']
    ordering = ['-create_date']

# Register your models here.
admin.site.register(CRO)
admin.site.register(Research_Management)
admin.site.register(Vendor)
admin.site.register(Supporting_type)
admin.site.register(Delivery)
admin.site.register(QC)
