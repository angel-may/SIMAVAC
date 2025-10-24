# biologicos_app/models.py
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.db import models


class Biologico(models.Model):
    idvacuna = models.AutoField(primary_key=True, db_column="idvacuna")
    nombre = models.CharField(max_length=100)
    dosisrequeridas = models.IntegerField(null=True, blank=True)
    intervalodias = models.IntegerField(null=True, blank=True)
    edadminimameses = models.IntegerField(null=True, blank=True)
    edadmaximameses = models.IntegerField(null=True, blank=True)
    restricciones = models.TextField(null=True, blank=True)
    idesquema = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = "biologico"  # 👈 nombre exacto de la tabla en PostgreSQL
        managed = False         # 👈 evita que Django intente crear o modificar esta tabla

    def __str__(self):
        return self.nombre or f"Biológico {self.idvacuna}"

class Almacen(models.Model):
    TIPO_CHOICES = (('general', 'General'), ('unidad', 'Unidad'))

    idalmacen = models.AutoField(primary_key=True)
    biologico = models.ForeignKey(Biologico, on_delete=models.CASCADE, related_name='movimientos')
    idunidad = models.IntegerField(blank=True, null=True)  # FK lógica a tabla de unidades (cuando exista)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    cantidad = models.IntegerField(validators=[MinValueValidator(0)])
    fecha_registro = models.DateTimeField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'almacen'
        ordering = ['-fecha_registro']
