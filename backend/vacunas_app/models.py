from django.db import models

class Vacuna(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fabricante = models.CharField(max_length=100, blank=True, null=True)
    dosis_requeridas = models.IntegerField(default=1)
    intervalo_dosis = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class PuntoVacunacion(models.Model):
    idpunto = models.AutoField(primary_key=True)
    idcampania = models.IntegerField(blank=True, null=True)
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    horario = models.CharField(max_length=50)
    responsable = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class RegistroVacunacion(models.Model):
    idregistro = models.AutoField(primary_key=True)
    nino_curp = models.CharField(max_length=18)
    nino_rfc = models.CharField(max_length=13)
    idvacuna = models.ForeignKey(Vacuna, on_delete=models.CASCADE)
    personal_curp = models.CharField(max_length=18)
    personal_rfc = models.CharField(max_length=13)
    fecha = models.DateField()
    dosis = models.IntegerField()
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('aplicada', 'Aplicada'),
        ('pendiente', 'Pendiente'),
        ('atrasada', 'Atrasada'),
    ])
    idcampania = models.IntegerField(blank=True, null=True)
    idpunto = models.IntegerField(blank=True, null=True)
    idunidad = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.nino_curp} - {self.idvacuna.nombre}"
