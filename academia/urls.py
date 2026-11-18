from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import GestionInscripcionesView

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
    path('registro/', views.registro, name='registro'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='academia/login.html'
        ),
        name='login'
    ),
    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),
    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),
    path(
        'gestion/',
        GestionInscripcionesView.as_view(),
        name='gestion'
    ),
]
