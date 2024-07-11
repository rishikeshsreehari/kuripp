# core/__init__.py
default_app_config = 'core.apps.CoreConfig'

# Import the signals to ensure they are registered when the app is ready
from . import signals
