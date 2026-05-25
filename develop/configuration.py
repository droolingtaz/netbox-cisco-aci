"""Minimal NetBox configuration used by the CI matrix and local dev."""

import os

ALLOWED_HOSTS = ["*"]

DATABASE = {
    "NAME": os.environ.get("DB_NAME", "netbox"),
    "USER": os.environ.get("DB_USER", "netbox"),
    "PASSWORD": os.environ.get("DB_PASSWORD", "netbox"),
    "HOST": os.environ.get("DB_HOST", "localhost"),
    "PORT": os.environ.get("DB_PORT", "5432"),
}

REDIS = {
    "tasks": {
        "HOST": os.environ.get("REDIS_HOST", "localhost"),
        "PORT": int(os.environ.get("REDIS_PORT", "6379")),
        "DATABASE": 0,
        "SSL": False,
    },
    "caching": {
        "HOST": os.environ.get("REDIS_HOST", "localhost"),
        "PORT": int(os.environ.get("REDIS_PORT", "6379")),
        "DATABASE": 1,
        "SSL": False,
    },
}

SECRET_KEY = "ci-only-secret-key-do-not-use-in-production-1234567890abcdefghij"

PLUGINS = ["netbox_aci"]

PLUGINS_CONFIG = {
    "netbox_aci": {},
}

# django-storages compatibility — kept local for the dev/CI loop.
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
