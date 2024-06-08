import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto
from .forms import ProductoForm

def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'listar.html', {'productos': productos})

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear.html', {'form': form})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar.html', {'form': form})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'eliminar.html', {'producto': producto})

def exportar_productos_csv(request):
    productos = Producto.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Precio', 'Cantidad'])

    for producto in productos:
        writer.writerow([producto.nombre, producto.precio, producto.cantidad])

    return response
def importar_productos_csv(request):
    if request.method == 'POST':
        archivo_csv = request.FILES.get('archivo_csv')
        if archivo_csv and archivo_csv.name.endswith('.csv'):
            file_data = archivo_csv.read().decode('utf-8')
            csv_data = file_data.split('\n')
            nombres_csv = [linea.split(',')[0] for linea in csv_data[1:] if linea]

            # Obtener una lista de todos los nombres de productos existentes
            nombres_existentes = Producto.objects.values_list('nombre', flat=True)

            # Eliminar los productos que ya no están en el archivo CSV
            productos_eliminar = Producto.objects.exclude(nombre__in=nombres_csv)
            productos_eliminar.delete()

            for linea in csv_data[1:]:
                if linea:
                    datos = linea.split(',')
                    nombre, precio, cantidad = datos
                    producto, creado = Producto.objects.get_or_create(
                        nombre=nombre,
                        defaults={
                            'precio': precio,
                            'cantidad': int(cantidad)
                        }
                    )
                    if not creado:
                        producto.precio = precio
                        producto.cantidad = int(cantidad)
                        producto.save()

            messages.success(request, 'Productos importados correctamente.')
        else:
            messages.error(request, 'Solo se permiten archivos CSV.')
    return redirect('listar_productos')