from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html

from .models import Curso, Inscripcion


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'cupos',
        'activo',
        'cantidad_inscripciones',
        'fecha_creacion',
    )
    list_filter = ('activo',)
    search_fields = ('codigo', 'nombre')
    readonly_fields = ('fecha_creacion', 'cantidad_inscripciones')
    list_per_page = 10

    @admin.display(description='Inscripciones')
    def cantidad_inscripciones(self, obj):
        return obj.inscripciones.count()


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = (
        'nombre_estudiante',
        'correo',
        'curso',
        'estado_coloreado',
        'fecha_solicitud',
    )
    list_filter = (
        'estado',
        'curso',
        'fecha_solicitud',
    )
    search_fields = (
        'nombre_estudiante',
        'correo',
        'curso__nombre',
    )
    readonly_fields = ('fecha_solicitud',)
    list_select_related = ('curso',)
    list_per_page = 10
    actions = [
        'aprobar_inscripciones',
        'rechazar_inscripciones',
    ]

    @admin.display(description='Estado')
    def estado_coloreado(self, obj):
        colores = {
            'pendiente': '#a16800',
            'aprobada': '#247a43',
            'rechazada': '#a72b55',
        }
        color = colores.get(obj.estado, '#75748c')
        return format_html(
            '<strong style="color: {};">{}</strong>',
            color,
            obj.get_estado_display(),
        )

    @admin.action(description='Aprobar inscripciones seleccionadas')
    def aprobar_inscripciones(self, request, queryset):
        pendientes = queryset.filter(estado='pendiente')
        cantidad = pendientes.update(estado='aprobada')
        self.message_user(
            request,
            f'{cantidad} inscripciones aprobadas.',
            messages.SUCCESS,
        )

    @admin.action(description='Rechazar inscripciones seleccionadas')
    def rechazar_inscripciones(self, request, queryset):
        pendientes = queryset.filter(estado='pendiente')
        cantidad = pendientes.update(estado='rechazada')
        self.message_user(
            request,
            f'{cantidad} inscripciones rechazadas.',
            messages.SUCCESS,
        )
