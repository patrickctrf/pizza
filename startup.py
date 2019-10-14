import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pizza.settings')

from django.core.management import execute_from_command_line


import django
django.setup()

from delivery.models import *

import datetime
from django.utils import timezone


