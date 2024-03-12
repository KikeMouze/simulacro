from django.shortcuts import render
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views import generic
from django.db.models import Q
from .models import Departamento
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django import forms
from django.http import HttpResponse
from openpyxl import Workbook
def index(request):
    """
    Función vista para la página inicio del sitio.
    """
    cantidadDepartamento = Departamento.objects.all().count()
  
    return render(
        request,
        'index.html',
        context={'cantidadDepartamento': cantidadDepartamento, }
    )
@method_decorator(never_cache, name='dispatch')
class departamentoListView(generic.ListView):
   model = Departamento
   permission_required = 'empresa.add_departamento'

   paginate_by = 2

   def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = super().get_queryset()

        if query:
            # Filtrar por nombre o descripcion si hay una consulta de búsqueda
            queryset = queryset.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))

        return queryset

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class departamentoCreate(PermissionRequiredMixin,CreateView):
    model = Departamento
    fields = ['nombre', 'descripcion']
    permission_required = 'empresa.add_departamento'
    def form_valid(self, form):
    # Puedes realizar acciones adicionales aquí antes de guardar el formulario
        return super().form_valid(form)

    def get_success_url(self):
    # Redirige a la página de detalle del estudiante después de la creación
        return reverse_lazy('departamento-detail', kwargs={'pk': self.object.pk})   


@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class departamentoDetailView(generic.DetailView):
    model = Departamento
    context_object_name = 'departamento'

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class departamentoUpdate(LoginRequiredMixin, UpdateView):
    model = Departamento
    fields = ['nombre', 'descripcion']
    # Método opcional para agregar lógica adicional antes de guardar el formulario
    def form_valid(self, form):
    # Puedes realizar acciones adicionales aquí antes de guardar el formulario
        return super().form_valid(form)
    # Sobrescribe el método get_success_url para proporcionar la URL de redirección
    def get_success_url(self):
        return reverse_lazy('departamento-update', kwargs={'pk': self.object.pk})
    

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch') 
class departamentoDelete(LoginRequiredMixin, DeleteView):
    model = Departamento
    success_url = reverse_lazy('departamento')
    permission_required = 'empresa.delete_departamento'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            # Manejar errores aquí si es necesario
            pass

@login_required
def reportes(request):
    response = render(request, 'reportes.html',)
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'  # HTTP 1.1.
    response['Pragma'] = 'no-cache'  # HTTP 1.0.
    response['Expires'] = '0'  # Proxies.
    return response

@login_required
def reporte_departamento(request):
    departamentos = Departamento.objects.all()
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="reporte_departamento.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "Departamento"

    # Encabezados
    ws.append(["nombre", "descripcion"])

    # Datos
    for deparmento in departamentos:
        ws.append([
            deparmento.nombre,
            deparmento.descripcion,
            
        ])

    wb.save(response)
    return response

from django.http import HttpResponse
from reportlab.pdfgen import canvas

def generar_pdf(request):
    # Obtener los datos del departamento (suponiendo que haya un solo departamento para este ejemplo)
    departamento = Departamento.objects.first()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ejemplo.pdf"'

    # Creamos un objeto canvas de ReportLab
    p = canvas.Canvas(response)

    # Agregamos texto al PDF
    p.drawString(100, 750, "Universidad UISRAEL")
    p.drawString(100, 730, "Nombre del departamento: {}".format(departamento.nombre))
    p.drawString(100, 710, "Descripción del departamento: {}".format(departamento.descripcion))
    # Puedes ajustar las coordenadas y la separación entre líneas según tus preferencias

    # Cerramos el objeto canvas
    p.showPage()
    p.save()

    return response


def lista_departamentos(request):
    query = request.GET.get('q', '')
    nombre = request.GET.get('nombre', '')
    descripcion = request.GET.get('descripcion', '')

    # Obtener todos los departamentos
    departamentos = Departamento.objects.all()

    # Obtener nombres y descripciones únicos
    nombres = departamentos.values_list('nombre', flat=True).distinct()
    descripciones = departamentos.values_list('descripcion', flat=True).distinct()

    # Aplicar filtro de búsqueda general
    if query:
        departamentos = departamentos.filter(nombre__icontains=query) | departamentos.filter(descripcion__icontains=query)

    # Aplicar filtros adicionales si se proporcionan valores en la solicitud
    if nombre:
        departamentos = departamentos.filter(nombre=nombre)
    if descripcion:
        departamentos = departamentos.filter(descripcion__icontains=descripcion)

    return render(request, 'departamento_list.html', {'object_list': departamentos, 'query': query, 'nombre': nombre, 'descripcion': descripcion, 'nombres': nombres, 'descripciones': descripciones})






from django.utils import timezone

def buscar_departamento(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    año = request.GET.get('año')
    if fecha_inicio and fecha_fin:
        # Convertir las fechas ingresadas a objetos datetime
        fecha_inicio_dt = timezone.make_aware(timezone.datetime.strptime(fecha_inicio, '%Y-%m-%d'))
        fecha_fin_dt = timezone.make_aware(timezone.datetime.strptime(fecha_fin, '%Y-%m-%d'))
        
        # Filtrar los departamentos con el rango de fechas proporcionado por el usuario
        departamentos = Departamento.objects.filter(campo_fecha__date__range=(fecha_inicio_dt.date(), fecha_fin_dt.date()))
    else:
        departamentos = None
    
    if año:
        # Filtrar los departamentos por el año proporcionado por el usuario
        departamentos = Departamento.objects.filter(campo_fecha__year=año)
    else:
        departamentos = None


    año_inicio = request.GET.get('año_inicio')
    año_fin = request.GET.get('año_fin')

    if año_inicio and año_fin:
        # Filtrar los departamentos por el rango de años proporcionado por el usuario
        departamentos = Departamento.objects.filter(campo_fecha__year__range=(año_inicio, año_fin))
    else:
        departamentos = None   

    return render(request, 'empresa/buscar_departamento.html', {'departamentos': departamentos})

