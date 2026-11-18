from django.urls import path

from . import views

app_name = 'academia'

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path(
        'cursos/',
        views.cursos,
        name='cursos'
    ),

    path(
        'consulta/',
        views.consulta,
        name='consulta'
    ),

    path(
        'inscripcion/',
        views.inscripcion,
        name='inscripcion'
    ),

    path(
        'inscripcion/exitosa/',
        views.inscripcion_exitosa,
        name='misolicitud_exito'
    ),
]
