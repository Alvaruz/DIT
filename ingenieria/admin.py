from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(Recurrente)
class RecurrenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'telefono', )
    list_filter = ('id', 'nombre', 'apellido', 'telefono', )


@admin.register(Barrio)
class BarrioAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    list_filter = ('nombre', )


@admin.register(Calle)
class CalleAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo', 'sentido', 'numeracion',)
    list_filter = ('nombre', 'tipo', 'sentido', 'numeracion',)


@admin.register(Documento_referencia)
class MotivoAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    list_filter = ('nombre', )


@admin.register(Documento_estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    list_filter = ('nombre', )


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nro', 'fecha', 'estado',)
    list_filter = ('id', 'nro', 'fecha', 'estado',)


@admin.register(DocumentoInstance)
class InstanceAdmin(admin.ModelAdmin):
    list_display = ('documento',)
    list_filter = ('documento',)


@admin.register(Documento_mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('documento', 'fecha_entrada', 'fecha_salida',)
    list_filter = ('documento', 'fecha_entrada', 'fecha_salida',)


@admin.register(Evento_tipo)
class Evento_tipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'detalle', )
    list_filter = ('nombre', 'detalle', )


@admin.register(Cierre_tipo)
class Cierre_tipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', )
    list_filter = ('nombre', )


@admin.register(Informe_clase)
class Informe_tipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'detalle', )
    list_filter = ('nombre', 'detalle', )


@admin.register(InformeResultado)
class InformeResultadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'detalle',)
    list_filter = ('nombre', 'detalle',)


@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):
    list_display = ('nro', 'recurrente', 'resultado',)
    list_filter = ('nro', 'recurrente', 'resultado',)


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ('tabla', 'campo', 'anterior', 'nuevo',)
    list_filter = ('tabla', 'campo', 'anterior', 'nuevo',)


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'fecha_fin',)
    list_filter = ('nombre', 'fecha', 'fecha_fin',)


@admin.register(Camiones_tipo)
class Camiones_tipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'detalle', )
    list_filter = ('nombre', 'detalle', )


@admin.register(Herramientas_tipo)
class Herramientas_tipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'detalle', )
    list_filter = ('nombre', 'detalle', )


@admin.register(Suelo_tipo)
class Suelo_tipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'detalle', )
    list_filter = ('nombre', 'detalle', )


@admin.register(Cartel)
class Suelo_tipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'detalle', )
    list_filter = ('nombre', 'detalle', )


@admin.register(Destino)
class Suelo_tipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'acronimo', )
    list_filter = ('nombre', 'acronimo', )