
from django import forms

from .models import Curso, Inscripcion


# Formulario clásico
class ConsultaForm(forms.Form):

    nombre = forms.CharField(
        label='Nombre completo',
        max_length=120,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre completo'
        })
    )

    correo = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'placeholder': 'ejemplo@correo.com'
        })
    )

    asunto = forms.CharField(
        label='Asunto',
        max_length=150
    )

    mensaje = forms.CharField(
        label='Mensaje',
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Escribe tu consulta...'
        })
    )


# Formulario basado en modelo
class InscripcionForm(forms.ModelForm):

    class Meta:
        model = Inscripcion

        fields = [
            'nombre_estudiante',
            'correo',
            'curso',
            'motivo',
        ]

        labels = {
            'nombre_estudiante': 'Nombre del estudiante',
            'correo': 'Correo electrónico',
            'curso': 'Curso solicitado',
            'motivo': 'Motivo de inscripción',
        }

        widgets = {
            'nombre_estudiante': forms.TextInput(attrs={
                'placeholder': 'Nombre completo'
            }),
            'correo': forms.EmailInput(attrs={
                'placeholder': 'ejemplo@correo.com'
            }),
            'motivo': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': '¿Por qué deseas estudiar en ASTRAEA?'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['curso'].queryset = Curso.objects.filter(
            activo=True
        )