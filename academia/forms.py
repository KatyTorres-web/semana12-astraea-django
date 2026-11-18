
from django import forms

from .models import Curso, Inscripcion
from .validators import (
    sanitize_input,
    validar_nombre,
    validar_codigo_estudiante,
)


# Formulario clásico
class ConsultaForm(forms.Form):
    nombre = forms.CharField(
        label='Nombre completo',
        max_length=120,
        validators=[validar_nombre],
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
        min_length=10,
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Escribe tu consulta...'
        })
    )

    def clean_nombre(self):
        return sanitize_input(self.cleaned_data['nombre'])

    def clean_correo(self):
        return self.cleaned_data['correo'].strip().lower()

    def clean(self):
        cleaned_data = super().clean()

        asunto = cleaned_data.get('asunto')
        mensaje = cleaned_data.get('mensaje')

        if asunto and mensaje:
            if asunto.strip().lower() == mensaje.strip().lower():
                self.add_error(
                    'mensaje',
                    'El mensaje debe ser diferente al asunto.'
                )

        return cleaned_data


# Formulario basado en modelo
class InscripcionForm(forms.ModelForm):
    codigo_estudiante = forms.CharField(
        max_length=8,
        validators=[validar_codigo_estudiante],
        help_text='Ejemplo: AST-2026'
    )

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

    def clean_nombre_estudiante(self):
        nombre = sanitize_input(
            self.cleaned_data['nombre_estudiante']
        )
        validar_nombre(nombre)
        return nombre

    def clean_correo(self):
        return self.cleaned_data['correo'].strip().lower()

    def clean_motivo(self):
        motivo = sanitize_input(
            self.cleaned_data['motivo']
        )

        if len(motivo) < 20:
            raise forms.ValidationError(
                'El motivo debe tener al menos 20 caracteres.'
            )

        return motivo

    def clean(self):
        cleaned_data = super().clean()

        curso = cleaned_data.get('curso')
        correo = cleaned_data.get('correo')

        if curso and correo:
            if Inscripcion.objects.filter(
                curso=curso,
                correo__iexact=correo
            ).exists():
                raise forms.ValidationError(
                    'Ya existe una inscripción con este correo '
                    'para el curso seleccionado.'
                )

        return cleaned_data