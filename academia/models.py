
from django.db import models


class Curso(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True
    )

    nombre = models.CharField(max_length=120)

    descripcion = models.TextField()

    cupos = models.PositiveIntegerField(default=20)

    activo = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'


class Inscripcion(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name='inscripciones'
    )

    nombre_estudiante = models.CharField(
        max_length=120
    )

    correo = models.EmailField()

    motivo = models.TextField()

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='pendiente'
    )

    fecha_solicitud = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.nombre_estudiante} - {self.curso.nombre}'

    class Meta:
        ordering = ['-fecha_solicitud']
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        constraints = [
            models.UniqueConstraint(
                fields=['curso', 'correo'],
                name='inscripcion_unica_por_curso_correo'
            )
        ]