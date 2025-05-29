from django.contrib import admin
from .models import Image, Image_link, Page, protocol_upload, training_schedule, Material, MaterialDownload, MaterialCategory


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'description', 'create_date', 'link')
    list_display_links = ('link',)
    list_editable = ('category', 'description')


@admin.register(MaterialDownload)
class MaterialDownloadAdmin(admin.ModelAdmin):
    list_display = ('create_date', 'material', 'downloader')


admin.site.register(Image)
admin.site.register(Image_link)
admin.site.register(Page)
admin.site.register(protocol_upload)
admin.site.register(training_schedule)
admin.site.register(Material)
