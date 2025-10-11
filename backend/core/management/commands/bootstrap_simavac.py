from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction

DEFAULT_USERS = {
    "admin1": ("adminpass", "admin1@example.com", "admin", True, False),
    "enf1":   ("enfpass",   "enf1@example.com",   "enfermera", False, False),
    "doc1":   ("docpass",   "doc1@example.com",   "doctor",    False, False),
    "tutor1": ("tutorpass", "tutor1@example.com", "tutor",     False, False),
    "root":   ("rootpass",  "root@example.com",   None, True, True),
}

GROUPS = ["admin", "enfermera", "doctor", "tutor"]

class Command(BaseCommand):
    help = "Crea grupos y usuarios de prueba para SIMAVAC"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-passwords",
            action="store_true",
            help="Reestablece las contraseñas de los usuarios por defecto",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        # Grupos
        for g in GROUPS:
            Group.objects.get_or_create(name=g)
        self.stdout.write(self.style.SUCCESS(f"Grupos verificados/creados: {', '.join(GROUPS)}"))

        # Usuarios
        for username, (pwd, email, group_name, is_staff, is_superuser) in DEFAULT_USERS.items():
            user, created = User.objects.get_or_create(username=username, defaults={
                "email": email,
                "is_active": True,
                "is_staff": is_staff or is_superuser,
                "is_superuser": is_superuser,
            })

            if created:
                user.set_password(pwd)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Usuario creado: {username}"))
            else:
                changed = False
                if options["reset_passwords"]:
                    user.set_password(pwd); changed = True
                if user.email != email:
                    user.email = email; changed = True
                if user.is_staff != (is_staff or is_superuser):
                    user.is_staff = (is_staff or is_superuser); changed = True
                if user.is_superuser != is_superuser:
                    user.is_superuser = is_superuser; changed = True
                if not user.is_active:
                    user.is_active = True; changed = True
                if changed:
                    user.save()
                    self.stdout.write(self.style.WARNING(f"Usuario actualizado: {username}"))

            if group_name:
                group = Group.objects.get(name=group_name)
                if not user.groups.filter(id=group.id).exists():
                    user.groups.add(group)
                    self.stdout.write(self.style.SUCCESS(f"Asignado {username} → grupo '{group_name}'"))

        self.stdout.write(self.style.SUCCESS("Bootstrap SIMAVAC completado."))
        self.stdout.write(self.style.NOTICE(
            "Credenciales de prueba:\n"
            "  - root / rootpass (superusuario)\n"
            "  - admin1 / adminpass (grupo: admin)\n"
            "  - enf1 / enfpass   (grupo: enfermera)\n"
            "  - doc1 / docpass   (grupo: doctor)\n"
            "  - tutor1 / tutorpass (grupo: tutor)"
        ))
