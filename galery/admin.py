from django.contrib import admin
from .models import Metadatos

@admin.register(Metadatos)
class MetadatosAdmin(admin.ModelAdmin):
    list_display = ('imagen', 'format', 'size', 'mode', 'created_at')
    list_filter = ('created_at', 'format', 'mode')
    search_fields = ('image_path',)
    readonly_fields = ('image_path', 'format', 'size', 'mode', 'exif_metadata', 'gps_data', 'created_at')
