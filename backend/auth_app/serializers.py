from rest_framework import serializers
from .models import Persona, Usuario, Rol
from django.contrib.auth.hashers import make_password


# ============================================================
# 🧩 SERIALIZER: Rol
# ============================================================
class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = ['idrol', 'nombre', 'estado']


# ============================================================
# 🧩 SERIALIZER: Persona
# ============================================================
class PersonaSerializer(serializers.ModelSerializer):
    rol = RolSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = '__all__'


# ============================================================
# 🧩 SERIALIZER: Usuario
# ============================================================
class UsuarioSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)
    rol = RolSerializer(read_only=True)

    class Meta:
        model = Usuario
        fields = ['username', 'password', 'persona', 'rol']
        extra_kwargs = {'password': {'write_only': True}}


# ============================================================
# 🧩 SERIALIZER: Login
# ============================================================
class LoginSerializer(serializers.Serializer):
    user = serializers.CharField()
    password = serializers.CharField(write_only=True)


# ============================================================
# 🧩 SERIALIZER: Registro (Persona + Usuario)
# ============================================================
class RegisterSerializer(serializers.Serializer):
    # Campos de Persona
    curp = serializers.CharField(max_length=18)
    rfc = serializers.CharField(max_length=13, required=False, allow_blank=True)
    nom = serializers.CharField(max_length=50)
    app = serializers.CharField(max_length=50, required=False, allow_blank=True)
    apm = serializers.CharField(max_length=50, required=False, allow_blank=True)
    sexo = serializers.CharField(max_length=1)
    tel = serializers.CharField(max_length=20, required=False, allow_blank=True)
    correo = serializers.EmailField()
    fnac = serializers.DateField(required=False, allow_null=True)
    tsangre = serializers.CharField(max_length=5, required=False, allow_blank=True)
    direc = serializers.CharField(max_length=255, required=False, allow_blank=True)
    rol = serializers.IntegerField()

    # Campos de Usuario
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(write_only=True)

    # ============================================================
    # ✅ CREAR PERSONA + USUARIO
    # ============================================================
    def create(self, validated_data):
        # Obtener rol
        try:
            rol = Rol.objects.get(idrol=validated_data['rol'])
        except Rol.DoesNotExist:
            raise serializers.ValidationError({"rol": "El rol seleccionado no existe."})

        # Convertir direc vacío a None (para evitar error tipo integer)
        direc_val = validated_data.get('direc')
        if direc_val in ["", None]:
            direc_val = None

        # Crear Persona
        persona = Persona.objects.create(
            curp=validated_data['curp'],
            rfc=validated_data.get('rfc', validated_data['curp'][:10]),
            nom=validated_data['nom'],
            app=validated_data.get('app', ''),
            apm=validated_data.get('apm', ''),
            sexo=validated_data['sexo'],
            tel=validated_data.get('tel', ''),
            correo=validated_data['correo'],
            fnac=validated_data.get('fnac', None),
            tsangre=validated_data.get('tsangre', ''),
            direc=direc_val,  # ✅ ahora controlado
            rol=rol
        )

        # Crear Usuario vinculado
        Usuario.objects.create(
            curp=persona.curp,
            rfc=persona.rfc,
            username=validated_data['username'],
            password=make_password(validated_data['password']),
            rol=rol
        )

        return {"message": "Usuario registrado correctamente."}

