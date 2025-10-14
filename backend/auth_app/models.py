from django.db import models


# ============================================================
# 🧩 MODELO: Rol
# ============================================================
class Rol(models.Model):
    idrol = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    detalles = models.TextField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=[('habilitado', 'Habilitado'), ('inhabilitado', 'Inhabilitado')]
    )
    idespecialidad = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'rol'

    def __str__(self):
        return self.nombre


# ============================================================
# 🧩 MODELO: Persona
# ============================================================
class Persona(models.Model):
    curp = models.CharField(max_length=18, primary_key=True)  # clave primaria real
    rfc = models.CharField(max_length=13)
    nom = models.CharField(max_length=50)
    homocv = models.CharField(max_length=5, blank=True, null=True)
    app = models.CharField(max_length=50, blank=True, null=True)
    apm = models.CharField(max_length=50, blank=True, null=True)
    sexo = models.CharField(max_length=1, choices=[('H', 'Hombre'), ('M', 'Mujer')])
    tel = models.CharField(max_length=20, blank=True, null=True)
    correo = models.CharField(unique=True, max_length=100)
    fnac = models.DateField(blank=True, null=True)
    tsangre = models.CharField(max_length=5, blank=True, null=True)
    direc = models.CharField(max_length=255, blank=True, null=True)  # texto libre
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='rol')

    class Meta:
        db_table = 'persona'
        unique_together = (('curp', 'rfc'),)

    def __str__(self):
        return f"{self.nom} {self.app or ''} {self.apm or ''}".strip()


# ============================================================
# 🧩 MODELO: Usuario
# ============================================================
class Usuario(models.Model):
    idusuario = models.AutoField(primary_key=True)  # 🔑 clave principal real
    curp = models.CharField(max_length=18)
    rfc = models.CharField(max_length=13)
    username = models.CharField(unique=True, max_length=50)
    password = models.CharField(max_length=255)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE, db_column='rol')

    class Meta:
        db_table = 'usuario'
        managed = True
        unique_together = (('curp', 'rfc'),)

    def __str__(self):
        return self.username
