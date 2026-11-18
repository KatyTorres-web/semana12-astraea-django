import re

from django.core.exceptions import ValidationError


def sanitize_input(texto):
    """Normaliza espacios sin alterar el contenido original."""
    return ' '.join(texto.strip().split())


def validar_nombre(valor):
    if not re.fullmatch(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ ]+", valor):
        raise ValidationError(
            'El nombre solo puede contener letras y espacios.'
        )


def validar_codigo_estudiante(valor):
    if not re.fullmatch(r"AST-\d{4}", valor):
        raise ValidationError(
            'Formato inválido. Ejemplo: AST-2026.'
        )
