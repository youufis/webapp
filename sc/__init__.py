import os
from django.apps import AppConfig


default_app_config = 'sc.ScConfig'

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]

class ScConfig(AppConfig):
    name = 'sc'
    verbose_name = "系统"

