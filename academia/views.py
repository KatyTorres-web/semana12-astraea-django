from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from .forms import ConsultaForm, InscripcionForm
from .models import Curso


# Página de inicio
def inicio(request):
    contexto = {
        'titulo': 'Bienvenido a ASTRAEA',
        'total_cursos': Curso.objects.filter(
            activo=True
        ).count(),
    }

    return render(
        request,
        'academia/inicio.html',
        contexto
    )


# Catálogo de cursos
def cursos(request):
    contexto = {
        'cursos': Curso.objects.filter(activo=True)
    }

    return render(
        request,
        'academia/cursos.html',
        contexto
    )


# Formulario clásico
@require_http_methods(['GET', 'POST'])
def consulta(request):

    if request.method == 'POST':
        form = ConsultaForm(request.POST)

        if form.is_valid():
            datos = form.cleaned_data

            return render(
                request,
                'academia/consulta_recibida.html',
                {
                    'nombre': datos['nombre'],
                    'asunto': datos['asunto'],
                }
            )

    else:
        form = ConsultaForm()

    return render(
        request,
        'academia/consulta.html',
        {'form': form}
    )


# Formulario ModelForm
@require_http_methods(['GET', 'POST'])
def inscripcion(request):

    if request.method == 'POST':
        form = InscripcionForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Tu solicitud de inscripción fue registrada correctamente.'
            )

            return redirect('academia:misolicitud_exito')

    else:
        form = InscripcionForm()

    return render(
        request,
        'academia/inscripcion.html',
        {'form': form}
    )


# Confirmación después del registro
def inscripcion_exitosa(request):
    return render(
        request,
        'academia/inscripcion_exitosa.html'
    )