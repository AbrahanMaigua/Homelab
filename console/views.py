# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
import subprocess, json


def consola_page(request):
    return render(request, "consola.html")

@csrf_exempt  # Si estás en desarrollo puedes desactivar CSRF, en producción usa el token.
def consola(request):
    if request.method == "POST":
        comando = request.POST.get("comando")

        # Manejo de imágenes: si el comando es 'img'
        if comando and comando.startswith("img "):  # Verifica que 'comando' no sea None y empieza con 'img '
            src = comando.split(' ')[-1].replace('\\', '/',)  # Extrae la ruta de la imagen
            if not src.startswith('http'):
                src = 'http://localhost:8000/media/imagenes/' + src.split('/')[-1]

            print(src)
            img = f"<img src='{src}' alt='Imagen cargada'>"  # Etiqueta de la imagen HTML

            # Aquí podrías agregar alguna lógica para mostrar la imagen en el frontend si es necesario
            return JsonResponse({"resultado": img})  # Retorna la imagen generada

        try:
            # Ejecuta el comando en el sistema
            resultado = subprocess.check_output(comando, shell=True, stderr=subprocess.STDOUT, text=True)

            # Si deseas mostrar el resultado como texto, puedes devolverlo tal cual
            return JsonResponse({"resultado": resultado})

        except subprocess.CalledProcessError as e:
            # Si ocurre un error al ejecutar el comando
            return JsonResponse({"error": f"Error ejecutando el comando: {e.output}"}, status=500)

        except Exception as e:
            # Captura cualquier otra excepción no esperada
            return JsonResponse({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=500)

    # Si el método no es POST, responde con error 405 (Método no permitido)
    return JsonResponse({"error": "Método no permitido"}, status=405)
