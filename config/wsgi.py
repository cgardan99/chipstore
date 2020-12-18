"""
WSGI config for Chipstore project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys
import environ
from pathlib import Path

from django.core.wsgi import get_wsgi_application

env = environ.Env()
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
WSGI_PATH = environ.Path(__file__)  # radon/radon/config/wsgi.py
ROOT_DIR = ROOT_DIR = WSGI_PATH - 2
sys.path.append(str(ROOT_DIR / "chipstore"))

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    env.read_env(env_file)
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        env('DJANGO_SETTINGS_MODULE')
    )
else:
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE", "radon.config.settings.production"
    )

application = get_wsgi_application()
