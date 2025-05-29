from django.contrib import admin
from .models import AuditEntry, Contact, InvestigatorContact

# Register your models here.
@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ['action','time', 'username']
    list_filter = ['action']

admin.site.register(Contact)
admin.site.register(InvestigatorContact)
