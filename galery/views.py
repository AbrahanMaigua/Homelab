from django.shortcuts import render, redirect
from .forms import ImagenConMetadatosForm
from .models import Metadatos

def cargar_imagen(request):
    if request.method == 'POST' and request.FILES['imagen']:
        form = ImagenConMetadatosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_imagenes')  # Redirige después de guardar
    else:
        form = ImagenConMetadatosForm()
        
    return render(request, 'cargar_imagen.html', {'form': form})

def lista_imagenes(request):
    imagenes = Metadatos.objects.all()
    return render(request, 'lista_imagenes.html', {'imagenes': imagenes})

