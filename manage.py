#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import django
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INSTALLED_APPS = ["orm", "query_engine", "visualize"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": f"{BASE_DIR}/stonksdb.sqlite3",
    }
}


def setup_orm():
    """
    Sets up the Django ORM without the web components with it
    """
    settings.configure(
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES=DATABASES,
    )

    django.setup()


def main():
    """Run administrative tasks."""
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stonks.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    setup_orm()
    main()
