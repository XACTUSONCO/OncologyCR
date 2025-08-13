from django.contrib import admin
from .models import Patient, Leave
from user.models import Contact
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from user.models import User
from django import forms
from django.db.models import Case, When

admin.site.register(Patient)

class LeaveResource(resources.ModelResource):
    class Meta:
        model = Leave

class CustomUserChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.username} | {obj.get_full_name()}"

class LeaveAdmin(ImportExportModelAdmin):
    resource_class = LeaveResource
    list_filter = ['is_deleted']
    list_display = ['is_deleted', 'name', 'from_date', 'kind']
    ordering = ['-from_date']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            contacts = Contact.objects.filter(
                onco_A=True,
                user__is_active=True
            ).select_related('user').order_by('name')

            user_ids = [c.user.id for c in contacts if c.user]

            preserved_order = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(user_ids)])
            users = User.objects.filter(id__in=user_ids).order_by(preserved_order)

            return CustomUserChoiceField(queryset=users)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Leave, LeaveAdmin)
