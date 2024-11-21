import os

def list_dir(path):
    """Lista los archivos y directorios en una ruta especificada."""
    try:
        return os.listdir(path)
    except FileNotFoundError:
        return f"Error: El directorio '{path}' no existe."
    except PermissionError:
        return f"Error: No tienes permisos para acceder a '{path}'."

def delete(path):
    """Elimina un archivo especificado."""
    try:
        os.remove(path)
        return f"Archivo '{path}' eliminado exitosamente."
    except FileNotFoundError:
        return f"Error: El archivo '{path}' no existe."
    except PermissionError:
        return f"Error: No tienes permisos para eliminar '{path}'."

def delete_all(path):
    """Elimina un directorio y su contenido."""
    try:
        os.removedirs(path)
        return f"Directorio '{path}' eliminado exitosamente."
    except FileNotFoundError:
        return f"Error: El directorio '{path}' no existe."
    except OSError:
        return f"Error: El directorio '{path}' no está vacío o no puede eliminarse."

def rename(src, dst):
    """Renombra o mueve un archivo o directorio."""
    try:
        os.rename(src, dst)
        return f"'{src}' renombrado/movido a '{dst}'."
    except FileNotFoundError:
        return f"Error: '{src}' no existe."
    except PermissionError:
        return f"Error: No tienes permisos para renombrar/mover '{src}'."

def mkdir(path):
    """Crea un nuevo directorio."""
    try:
        os.mkdir(path)
        return f"Directorio '{path}' creado exitosamente."
    except FileExistsError:
        return f"Error: El directorio '{path}' ya existe."
    except PermissionError:
        return f"Error: No tienes permisos para crear '{path}'."

def cwd():
    """Devuelve el directorio de trabajo actual."""
    return {
        'cwd': os.getcwd(),
        'cwdb': os.getcwdb(),
    }

def scandir(path):
    """Lista los archivos en un directorio, excluyendo los ocultos."""
    try:
        with os.scandir(path) as it:
            return [entry.name for entry in it if not entry.name.startswith('.') and entry.is_file()]
    except FileNotFoundError:
        return f"Error: El directorio '{path}' no existe."
    except PermissionError:
        return f"Error: No tienes permisos para acceder a '{path}'."
