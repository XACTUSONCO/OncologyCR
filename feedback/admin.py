from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Feedback, Assignment, UploadRECIST
from .resources import AssignmentResource, FeedbackResource


class AssignmentAdmin(ImportExportModelAdmin):
    resource_class = AssignmentResource
    list_display = ('status', 'no', 'register_number', 'name', 'sex', 'age', 'dx', 'previous_tx', 'ECOG',
                    'is_deleted', 'create_date', 'update_date', 'crc', 'research', 'curr_crc')


class FeedbackAdmin(ImportExportModelAdmin):
    resource_class = FeedbackResource
    list_display = ('cycle', 'dosing_date', 'next_visit', 'tx_dose', 'photo_date', 'response', 'response_text', 'get_FU', 'eos', 'is_accompany',
                    'toxicity', 'comment', 'create_date', 'update_date', 'assignment')

    def get_FU(self, obj):
        FU = [str(e) for e in obj.fu.all()]
        return '[' + ', '.join(FU) + ']'

class UploadRECISTAdmin(admin.ModelAdmin):
    model = UploadRECIST
    list_display = ('id', 'get_assignment', 'filename', 'assignment')

    def get_assignment(self, obj):
        return obj.assignment.id

    get_assignment.admin_order_field = 'assignemnt'  # Allows column order sorting
    get_assignment.short_description = 'Assignment'  # Renames column head

# Register your models here.
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(UploadRECIST, UploadRECISTAdmin)
