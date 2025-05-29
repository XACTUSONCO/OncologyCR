from django.contrib import admin
from .models import Research, Cancer, Lesion, \
    Alternation, Line, Chemotherapy, IO_Naive, Brain_METS, Biopsy, PDL1, Phase, Type, \
    UploadFile, UploadEngFile, UploadInclusion, UploadExclusion, UploadReference, History, WaitingList, research_WaitingList, ONCO_CR_COUNT, \
    Pre_Initiation, End_research, UploadImage, End_UploadImage, Research_Archive, End_Research_Archive, Route_of_Administration, DownloadLog


class ResearchAdmin(admin.ModelAdmin):
    model = Research
    list_display = (
        'id',
        'is_deleted',
        'is_recruiting',
        'get_type',
        'research_name',
        'research_explanation',
        'medicine_name',
        'get_cancer',
        'get_alternation',
        'get_line', 'get_chemotherapy', 'create_date',
        'update_date')

    def get_cancer(self, obj):
        cancer = [str(e) for e in obj.cancer.all()]
        return '[' + ', '.join(cancer) + ']'

    def get_type(self, obj):
        type = [str(e) for e in obj.type.all()]
        return '[' + ', '.join(type) + ']'

    def get_histology(self, obj):
        histology = [str(e) for e in obj.histology.all()]
        return '[' + ', '.join(histology) + ']'

    def get_ecog(self, obj):
        ecog = [str(e) for e in obj.ecog.all()]
        return '[' + ', '.join(ecog) + ']'

    def get_lesion(self, obj):
        lesion = [str(e) for e in obj.lesion.all()]
        return '[' + ', '.join(lesion) + ']'

    def get_alternation(self, obj):
        alternation = [str(e) for e in obj.alternation.all()]
        return '[' + ', '.join(alternation) + ']'

    def get_pdl1(self, obj):
        pdl1 = [str(e) for e in obj.pdl1.all()]
        return '[' + ', '.join(pdl1) + ']'

    def get_line(self, obj):
        line = [str(e) for e in obj.line.all()]
        return '[' + ', '.join(line) + ']'

    def get_chemotherapy(self, obj):
        chemotherapy = [str(e) for e in obj.chemotherapy.all()]
        return '[' + ', '.join(chemotherapy) + ']'

    def get_msi(self, obj):
        msi = [str(e) for e in obj.msi.all()]
        return '[' + ', '.join(msi) + ']'

    def get_io_naive(self, obj):
        io_naive = [str(e) for e in obj.io_naive.all()]
        return '[' + ', '.join(io_naive) + ']'

    get_cancer.short_description = 'Cancer'
    get_histology.short_description = 'Histology'
    get_lesion.short_description = 'Lesion'
    get_alternation.short_description = 'Alternation'
    get_ecog.short_description = 'ECOG'
    get_line.short_description = 'Line'
    get_chemotherapy.short_description = 'Chemotherapy'
    get_msi.short_description = 'MSI'
    get_io_naive.short_description = 'IO Naive'


class UploadFileAdmin(admin.ModelAdmin):
    model = UploadFile
    list_display = ('id', 'get_research', 'filename')

    def get_research(self, obj):
        return obj.research.id

    get_research.admin_order_field = 'research'  # Allows column order sorting
    get_research.short_description = 'Research'  # Renames column head

class UploadEngFileAdmin(admin.ModelAdmin):
    model = UploadEngFile
    list_display = ('id', 'get_research', 'filename')

    def get_research(self, obj):
        return obj.research.id

    get_research.admin_order_field = 'research'  # Allows column order sorting
    get_research.short_description = 'Research'  # Renames column head

class UploadInclusionAdmin(admin.ModelAdmin):
    model = UploadInclusion
    list_display = ('id', 'get_research', 'filename')

    def get_research(self, obj):
        return obj.research.id

    get_research.admin_order_field = 'research'  # Allows column order sorting
    get_research.short_description = 'Research'  # Renames column head

class UploadExclusionAdmin(admin.ModelAdmin):
    model = UploadExclusion
    list_display = ('id', 'get_research', 'filename')

    def get_research(self, obj):
        return obj.research.id

    get_research.admin_order_field = 'research'  # Allows column order sorting
    get_research.short_description = 'Research'  # Renames column head

class UploadReferenceAdmin(admin.ModelAdmin):
    model = UploadReference
    list_display = ('id', 'get_research', 'filename')

    def get_research(self, obj):
        return obj.research.id

    get_research.admin_order_field = 'research'  # Allows column order sorting
    get_research.short_description = 'Research'  # Renames column head


class HistoryAdmin(admin.ModelAdmin):
    model = History
    list_display = ('id', 'user', 'research', 'history_type', 'create_date', 'summary')


@admin.register(DownloadLog)
class DownloadLogAdmin(admin.ModelAdmin):
    list_display = ('content', 'create_date', 'downloader')


# Register your models here.
admin.site.register(Research, ResearchAdmin)

fields = [Cancer, Lesion, Alternation, Line, Chemotherapy,
          IO_Naive, Brain_METS, Biopsy, PDL1, Phase, Type, Route_of_Administration]
for field in fields:
    admin.site.register(field)

admin.site.register(UploadFile, UploadFileAdmin)
admin.site.register(UploadEngFile, UploadEngFileAdmin)
admin.site.register(UploadInclusion, UploadInclusionAdmin)
admin.site.register(UploadExclusion, UploadExclusionAdmin)
admin.site.register(UploadReference, UploadReferenceAdmin)

admin.site.register(History, HistoryAdmin)

admin.site.register(WaitingList)
admin.site.register(research_WaitingList)
admin.site.register(ONCO_CR_COUNT)
admin.site.register(Pre_Initiation)
admin.site.register(End_research)
admin.site.register(UploadImage)
admin.site.register(End_UploadImage)
admin.site.register(Research_Archive)
admin.site.register(End_Research_Archive)
