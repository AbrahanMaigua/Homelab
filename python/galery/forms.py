from django import forms
from .models import Metadatos
from lib.metadata import get_image_metadata, get_exif_metadata, get_gps_data

class ImagenConMetadatosForm(forms.ModelForm):
    class Meta:
        model = Metadatos
        fields = ['imagen']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            # Guarda la instancia para obtener la ruta completa de la imagen
            instance.save()

            # Ahora que la imagen se ha guardado, obtenemos su ruta correctamente
            image_path = instance.imagen.path  # Esto da la ruta completa en el sistema de archivos
            metadata = get_image_metadata(image_path)
            exif_metadata = get_exif_metadata(image_path)
            gps_data = get_gps_data(image_path)

            # Actualiza los campos con los metadatos
            instance.image_path = image_path  # La ruta completa de la imagen
            instance.format = metadata['format']
            instance.size = str(metadata['size'])  # Convertir a string
            instance.mode = metadata['mode']
            instance.exif_metadata = exif_metadata
            instance.gps_data = gps_data
            
            instance.save()  # Guarda la instancia nuevamente con los datos actualizados

        return instance
