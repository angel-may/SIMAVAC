"""
Django settings for simavac_core project.
"""

from pathlib import Path
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# ──────────────────────────────────────────────────────────────────────────────
# RUTAS BÁSICAS
# ──────────────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────────────────────────
# SEGURIDAD / DEBUG
# ──────────────────────────────────────────────────────────────────────────────
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-CHANGE-ME')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# ──────────────────────────────────────────────────────────────────────────────
# APPS
# ──────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # django...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # terceros
    'rest_framework',
    'corsheaders',

    # apps del proyecto
    'backend.core',
    'backend.admin_app',
    'backend.enfermera_app',
    'backend.doctor_app',
    'backend.tutor_app',
    'backend.auth_app',
    'backend.vacunas_app',
    'backend.biologicos_app',
]

# ──────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS primero
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simavac_core.urls'

# ──────────────────────────────────────────────────────────────────────────────
# TEMPLATES
# ──────────────────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # opcional
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simavac_core.wsgi.application'

# ──────────────────────────────────────────────────────────────────────────────
# BASE DE DATOS (PostgreSQL)
# ──────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# ──────────────────────────────────────────────────────────────────────────────
# AUTENTICACIÓN DRF + JWT
# ──────────────────────────────────────────────────────────────────────────────
# ──────────────────────────────────────────────────────────────────────────────
# AUTENTICACIÓN DRF + JWT
# ──────────────────────────────────────────────────────────────────────────────
from datetime import timedelta
from datetime import timedelta
import os

# ============================================================
# ⚙️ REST FRAMEWORK CONFIG
# ============================================================
from datetime import timedelta
import os
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'backend.auth_app.custom_auth.CustomJWTAuthentication',  # ✅ personalizada
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "SIGNING_KEY": os.getenv("SECRET_KEY", "django-insecure-CHANGE-ME"),
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
}



# ──────────────────────────────────────────────────────────────────────────────
# VALIDACIÓN DE CONTRASEÑAS
# ──────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# ──────────────────────────────────────────────────────────────────────────────
# INTERNACIONALIZACIÓN
# ──────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────────────────────────────────────
# ESTÁTICOS
# ──────────────────────────────────────────────────────────────────────────────
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ──────────────────────────────────────────────────────────────────────────────
# CORS / CSRF (para Vue en dev)
# ──────────────────────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True  # en producción, usar CORS_ALLOWED_ORIGINS

# Si usas CSRF con el frontend, añade el puerto de Vite:
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
