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

# NetBox 4.5 introduced API_TOKEN_PEPPERS — a dict mapping integer
# pepper IDs (0–32767) to string secrets used to digest API tokens.
# Each pepper must be at least 50 characters. The setting has no
# default and Token.save() raises if it's missing, so every API test
# fails without at least one valid pepper. CI-only value below; real
# deployments must set their own via environment.
API_TOKEN_PEPPERS = {
    1: "ci-only-pepper-do-not-use-in-production-0000000000000000000000000000000000",
}

PLUGINS = ["netbox_cisco_aci"]

PLUGINS_CONFIG = {
    "netbox_cisco_aci": {},
}

# django-storages compatibility — kept local for the dev/CI loop.
DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
