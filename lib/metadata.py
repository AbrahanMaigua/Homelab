import os
from PIL import Image, ExifTags
from galery.models import Metadatos  # Cambia 'myapp' por el nombre de tu aplicación

def make_serializable(value):
    """Convierte valores no serializables a tipos serializables."""
    if isinstance(value, tuple):  # Maneja tuplas (común en GPS)
        return [make_serializable(v) for v in value]
    elif isinstance(value, dict):  # Maneja diccionarios
        return {make_serializable(k): make_serializable(v) for k, v in value.items()}
    elif isinstance(value, bytes):  # Convierte valores en bytes a cadenas
        return str(value.decode('utf-8', errors='ignore'))
    return str(value)  # Retorna el valor tal cual si es serializable

def get_exif_metadata(image_path):
    """Obtiene los ImagenConMetadatos EXIF de la imagen."""
    with Image.open(image_path) as img:
        exif_data = img._getexif()

        if exif_data is not None:
            return {ExifTags.TAGS.get(tag, tag): make_serializable(value) for tag, value in exif_data.items()}
    return None

def get_image_metadata(image_path):
    """Obtiene los ImagenConMetadatos básicos de la imagen."""
    with Image.open(image_path) as img:
        return {
            'format': img.format,
            'size': f"{img.size[0]}x{img.size[1]}",
            'mode': img.mode,
        }

def get_gps_data(image_path):
    """Obtiene los datos GPS de la imagen."""
    with Image.open(image_path) as img:
        exif_data = img._getexif()

    if not exif_data:
        return None

    gps_info = None
    for tag, value in exif_data.items():
        if ExifTags.TAGS.get(tag, tag) == 'GPSInfo':
            gps_info = value
            break

    if gps_info:
        return {ExifTags.GPSTAGS.get(t, t): make_serializable(gps_info[t]) for t in gps_info}
    return None

import os
def save_metadata_to_db(instance):
    """Extrae los metadatos de una imagen y los guarda en el modelo Metadatos."""
    image_path = instance.imagen.path  # Ruta completa de la imagen cargada
    if not os.path.exists( image_path):
        raise FileNotFoundError(f"Image not found at {image_path}")

    metadata = get_image_metadata(image_path)
    exif_metadata = get_exif_metadata(image_path)
    gps_data = get_gps_data(image_path)

    # Actualiza o crea los datos en la base de datos
    instance.image_path = image_path
    instance.format = metadata['format']
    instance.size = metadata['size']
    instance.mode = metadata['mode']
    instance.exif_metadata = exif_metadata
    instance.gps_data = gps_data
    instance.save()

    print(f"Metadata for {image_path} saved to database.")
