from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .views import generar_pdf



urlpatterns = [
    path('', views.index, name='index'),
#CRUD DEPARTAMENTO
    # LISTA DE DEPARTAMENTO, CREAR, VISTA DE UNO, EDITAR Y ELIMINAR
    path('departamento/',login_required(views.departamentoListView.as_view()), name='departamento'),
    path('departamento/create/', login_required(views.departamentoCreate.as_view()), name='departamento-create'),
    path('departamento/<int:pk>/', login_required(views.departamentoDetailView.as_view()), name='departamento-detail'),
    path('departamento/<int:pk>/update/', login_required(views.departamentoUpdate.as_view()), name='departamento-update'),
    path('departamento/<int:pk>/delete/', login_required(views.departamentoDelete.as_view()), name='departamento-delete'),
    path('reportes/', views.reportes, name='reportes'),
    path('reportes/departamento/', views.reporte_departamento, name='reporte_departamento'),
    path('generar-pdf/', generar_pdf, name='generar_pdf'),
    path('buscar-departamento/', views.buscar_departamento, name='buscar-departamento'),

     # Otras rutas
    path('proyectos_asignados/', views.proyecto_asignado, name='proyectos-asignados'),
    path('proyectos_asignados_docente/', views.proyectos_asignados_docente, name='proyectos-asignados-docente'),
    path('proyecto/<int:proyecto_id>/reporte_estudiantes/', views.reporte_estudiantes, name='reporte_estudiantes'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
  