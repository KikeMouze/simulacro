from django.contrib import admin

from .models import Empleado,Departamento
from import_export import resources
from import_export.admin import ImportExportModelAdmin
class EmpleadoResource(resources.ModelResource):
    class Meta:
        model=Empleado
class EmpleadoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['cedula','nombre', 'apellido','edad','departamento']
    resource_class=EmpleadoResource

admin.site.register(Empleado, EmpleadoAdmin)

class DeparmentoResource(resources.ModelResource):
    class Meta:
        model=Departamento
class DepartamentoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display=['id','nombre','descripcion','archivo']
    resource=DeparmentoResource
admin.site.register(Departamento, DepartamentoAdmin)