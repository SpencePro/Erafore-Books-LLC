"""
WSGI config for erafore project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

user_name = os.environ.get('USER')
password = os.environ.get('PASSWORD')
secret_key = os.environ.get('SECRET_KEY')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erafore.settings')

application = get_wsgi_application()
