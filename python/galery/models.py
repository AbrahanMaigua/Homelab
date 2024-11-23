from django.db import models


class Metadatos(models.Model):
    imagen = models.ImageField(upload_to='imagenes/', verbose_name="Imagen")
    image_path = models.CharField(max_length=255, blank=True)
    format = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    mode = models.CharField(max_length=50, blank=True)
    exif_metadata = models.JSONField(null=True, blank=True)
    gps_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.imagen.name
